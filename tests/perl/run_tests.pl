#!/usr/bin/env perl
# SpectreBand Test Suite — Perl-based hardware simulation and validation
# Usage: prove -l tests/perl/
#        perl tests/perl/run_tests.pl

use strict;
use warnings;
use FindBin;
use lib "$FindBin::Bin/lib";

use Test::More;
use SpectreBand::Test::Harness;

my $harness = SpectreBand::Test::Harness->new(
    verbose => $ENV{VERBOSE} || 0,
    field_config => $ENV{FIELD_CONFIG} || 'fields/blitz_dacono/config.json',
);

# Run all test suites
$harness->run_suite('positioning');
$harness->run_suite('game_modes');
$harness->run_suite('hardware');
$harness->run_suite('network');

$harness->report;
done_testing();
