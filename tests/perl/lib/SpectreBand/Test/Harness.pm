package SpectreBand::Test::Harness;
# Test harness for SpectreBand validation

use strict;
use warnings;
use JSON::PP;
use Time::HiRes qw(time sleep);

sub new {
    my ($class, %args) = @_;
    my $self = {
        verbose => $args{verbose} || 0,
        field_config => $args{field_config},
        results => {},
        start_time => time(),
    };
    bless $self, $class;
    $self->_load_field_config;
    return $self;
}

sub _load_field_config {
    my ($self) = @_;
    if ($self->{field_config} && -f $self->{field_config}) {
        open my $fh, '<', $self->{field_config} or die "Cannot open $self->{field_config}: $!";
        local $/;
        my $json = <$fh>;
        close $fh;
        $self->{field} = decode_json($json);
        print "Loaded field config: $self->{field}{field_name}\n" if $self->{verbose};
    }
}

sub run_suite {
    my ($self, $suite_name) = @_;
    print "\n=== Running $suite_name tests ===\n" if $self->{verbose};
    
    my $suite_file = "tests/perl/t/$suite_name.t";
    if (-f $suite_file) {
        system("perl", "-I", "tests/perl/lib", $suite_file);
        $self->{results}{$suite_name} = $? == 0 ? 'PASS' : 'FAIL';
    } else {
        warn "Suite file not found: $suite_file\n";
        $self->{results}{$suite_name} = 'SKIP';
    }
}

sub report {
    my ($self) = @_;
    my $elapsed = time() - $self->{start_time};
    
    print "\n" . "="x60 . "\n";
    print "SPECTREBAND TEST REPORT\n";
    print "="x60 . "\n";
    print sprintf("%-20s %10s\n", "Suite", "Result");
    print "-"x60 . "\n";
    
    my ($pass, $fail, $skip) = (0, 0, 0);
    for my $suite (sort keys %{$self->{results}}) {
        my $result = $self->{results}{$suite};
        print sprintf("%-20s %10s\n", $suite, $result);
        $pass++ if $result eq 'PASS';
        $fail++ if $result eq 'FAIL';
        $skip++ if $result eq 'SKIP';
    }
    
    print "-"x60 . "\n";
    print "Total: " . ($pass + $fail + $skip) . " | Pass: $pass | Fail: $fail | Skip: $skip\n";
    print "Elapsed: " . sprintf("%.2f", $elapsed) . "s\n";
    print "="x60 . "\n";
    
    return $fail == 0;
}

1;
