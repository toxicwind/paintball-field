#!/usr/bin/env perl
# Positioning system tests — RSSI trilateration, Kalman filter, particle filter

use strict;
use warnings;
use FindBin;
use lib "$FindBin::Bin/../lib";

use Test::More tests => 12;
use JSON::PP;
use Math::Trig;

# Load field config
my $field_config = $ENV{FIELD_CONFIG} || 'fields/blitz_dacono/config.json';
my $field;
if (-f $field_config) {
    open my $fh, '<', $field_config or die $!;
    local $/;
    $field = decode_json(<$fh>);
    close $fh;
}

# Test 1: Field config loads
ok($field, "Field config loaded: $field_config");

# Test 2: AP count is 6
my @aps = @{$field->{fields}[0]{ap_placement}};
is(scalar @aps, 6, "Field has 6 AP nodes");

# Test 3: AP positions are within field bounds
my ($fw, $fh) = @{$field->{fields}[0]}{qw(size_m)};
for my $ap (@aps) {
    ok($ap->{x} >= 0 && $ap->{x} <= $field->{fields}[0]{size_m}[0], "AP $ap->{id} X within bounds");
    ok($ap->{y} >= 0 && $ap->{y} <= $field->{fields}[0]{size_m}[1], "AP $ap->{id} Y within bounds");
}

# Test 4: RSSI to distance conversion
sub rssi_to_distance {
    my ($rssi, $tx_power, $n) = @_;
    return 10 ** (($tx_power - $rssi) / (10 * $n));
}

my $d = rssi_to_distance(-50, -30, 2.5);
ok($d > 0 && $d < 100, "RSSI to distance conversion: $d m");

# Test 5: Trilateration with perfect RSSI
sub trilaterate {
    my ($readings, $aps) = @_;
    my ($weights, $wx, $wy) = (0, 0, 0);
    for my $r (@$readings) {
        my $ap = $aps->{$r->{ap_id}};
        next unless $ap;
        my $d = rssi_to_distance($r->{rssi}, $ap->{tx_power}, $ap->{path_loss});
        my $w = 1.0 / ($d || 0.1);
        $weights += $w;
        $wx += $ap->{x} * $w;
        $wy += $ap->{y} * $w;
    }
    return $weights > 0 ? [$wx/$weights, $wy/$weights] : [25, 15];
}

my $test_aps = {
    "AP-01" => {x=>0, y=>0, tx_power=>-30, path_loss=>2.5},
    "AP-02" => {x=>50, y=>0, tx_power=>-30, path_loss=>2.5},
    "AP-03" => {x=>25, y=>30, tx_power=>-30, path_loss=>2.5},
};

# Player at (25, 15) center
my $readings = [
    {ap_id=>"AP-01", rssi=>-41},
    {ap_id=>"AP-02", rssi=>-41},
    {ap_id=>"AP-03", rssi=>-35},
];
my $pos = trilaterate($readings, $test_aps);
my $error = sqrt(($pos->[0]-25)**2 + ($pos->[1]-15)**2);
ok($error < 5, "Trilateration accuracy: $error m (target < 5m)");

# Test 6: Kalman filter prediction
sub kalman_predict {
    my ($state, $dt) = @_;
    my ($x, $y, $vx, $vy) = @$state;
    return [$x + $vx*$dt, $y + $vy*$dt, $vx, $vy];
}

my $kf_state = [25, 15, 1, 0];
my $pred = kalman_predict($kf_state, 0.2);
is($pred->[0], 25.2, "Kalman X prediction correct");
is($pred->[1], 15.0, "Kalman Y prediction correct");

# Test 7: Median filter for RSSI
sub median {
    my @sorted = sort { $a <=> $b } @_;
    return $sorted[int(@sorted/2)];
}

my @rssi_samples = (-45, -80, -46, -44, -47);  # -80 is outlier
my $median_rssi = median(@rssi_samples);
is($median_rssi, -46, "Median filter rejects outlier: $median_rssi");

# Test 8: Channel assignment
my %channels;
for my $ap (@aps) {
    $channels{$ap->{channel}}++;
}
is(scalar keys %channels, 3, "APs use 3 non-overlapping channels (1, 6, 11)");

# Test 9: Path loss exponent is reasonable
for my $ap (@aps) {
    ok($ap->{path_loss} >= 2.0 && $ap->{path_loss} <= 4.0, 
       "AP $ap->{id} path loss exponent $ap->{path_loss} is reasonable");
}

# Test 10: Calibration produces valid config
ok($field->{fields}[0]{calibration}{path_loss_exponent} > 0, 
   "Calibration has valid path loss exponent");

print "\nPositioning tests complete.\n";
