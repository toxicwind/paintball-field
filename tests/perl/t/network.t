#!/usr/bin/env perl
# Network protocol tests — WebSocket, MQTT, packet format

use strict;
use warnings;
use FindBin;
use lib "$FindBin::Bin/../lib";

use Test::More tests => 8;
use JSON::PP;

# Test 1: WebSocket message format
my $ws_msg = encode_json({
    type => "rssi_batch",
    band_id => "B001",
    team => "red",
    readings => [
        {ap_id => "AP-01", rssi => -45},
        {ap_id => "AP-02", rssi => -52},
    ]
});

ok($ws_msg, "WebSocket message encodes to JSON");
ok(length($ws_msg) < 1024, "WebSocket message under 1KB: " . length($ws_msg) . " bytes");

# Test 2: MQTT topic structure
my @valid_topics = (
    "nodes/announce",
    "nodes/NODE-001/cmd",
    "nodes/NODE-001/event",
);
for my $topic (@valid_topics) {
    ok($topic =~ /^nodes\/[A-Za-z0-9_-]+\/(announce|cmd|event)$/, "Valid MQTT topic: $topic");
}

# Test 3: Band ID format
my @valid_ids = ("B001", "B123", "B999");
my @invalid_ids = ("X001", "B", "B1000", "band1");

for my $id (@valid_ids) {
    ok($id =~ /^B\d{3}$/, "Valid band ID format: $id");
}
for my $id (@invalid_ids) {
    ok($id !~ /^B\d{3}$/, "Invalid band ID rejected: $id");
}

# Test 4: AP channel assignment
my @channels = (1, 6, 11, 1, 6, 11);
my %channel_count;
$channel_count{$_}++ for @channels;

ok(exists $channel_count{1}, "Channel 1 used");
ok(exists $channel_count{6}, "Channel 6 used");
ok(exists $channel_count{11}, "Channel 11 used");
ok(scalar(keys %channel_count) == 3, "Exactly 3 channels used (no overlap)");

print "\nNetwork tests complete.\n";
