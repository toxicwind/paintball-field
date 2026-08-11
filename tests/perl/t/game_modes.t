#!/usr/bin/env perl
# Game mode validation tests — balance, rules, band behavior

use strict;
use warnings;
use FindBin;
use lib "$FindBin::Bin/../lib";

use Test::More;
use JSON::PP;

my $modes_dir = 'modes';
my @modes = qw(spectre hunter_prey ghost capture_flag domination search_destroy data_heist infection vip_escort battle_royale frontline overwatch tournament);

plan tests => scalar(@modes) * 4 + 2;

# Test 1: All mode configs exist and are valid JSON
for my $mode (@modes) {
    my $file = "$modes_dir/$mode/config.json";
    ok(-f $file, "Mode config exists: $mode");
    
    open my $fh, '<', $file or die $!;
    local $/;
    my $json = <$fh>;
    close $fh;
    
    my $cfg = eval { decode_json($json) };
    ok($cfg, "Mode config is valid JSON: $mode");
    
    # Test required fields
    ok($cfg->{name}, "Mode has name: $mode");
    ok(defined $cfg->{tier} && $cfg->{tier} >= 0 && $cfg->{tier} <= 3, 
       "Mode has valid tier (0-3): $mode");
}

# Test 2: Tier 0 modes require no additional hardware
my @tier0 = grep {
    my $f = "$modes_dir/$_/config.json";
    open my $fh, '<', $f or die $!;
    local $/;
    my $cfg = decode_json(<$fh>);
    close $fh;
    $cfg->{tier} == 0
} @modes;

is(scalar @tier0, 3, "Exactly 3 Tier 0 modes (band only)");

# Test 3: All modes have blitz_ready flag
for my $mode (@modes) {
    my $f = "$modes_dir/$mode/config.json";
    open my $fh, '<', $f or die $!;
    local $/;
    my $cfg = decode_json(<$fh>);
    close $fh;
    ok(defined $cfg->{blitz_ready}, "Mode has blitz_ready flag: $mode");
}

print "\nGame mode tests complete.\n";
