#!/usr/bin/env perl
# Hardware BOM validation tests — costs, parts, suppliers

use strict;
use warnings;
use FindBin;
use lib "$FindBin::Bin/../lib";

use Test::More;
use Text::CSV;

my @bom_files = (
    'hardware/band_v1.0/BOM.csv',
    'hardware/band_v1.1/BOM.csv', 
    'hardware/ap_node/BOM.csv',
    'hardware/charging_rack/BOM.csv',
);

plan tests => scalar(@bom_files) * 3 + 1;

my $total_cost = 0;

for my $bom_file (@bom_files) {
    ok(-f $bom_file, "BOM file exists: $bom_file");
    
    my $csv = Text::CSV->new({ binary => 1, auto_diag => 1 });
    open my $fh, '<', $bom_file or die $!;
    
    my $header = $csv->getline($fh);
    ok($header && scalar(@$header) >= 4, "BOM has valid header: $bom_file");
    
    my $file_total = 0;
    while (my $row = $csv->getline($fh)) {
        next unless $row->[4] && $row->[4] =~ /^\d+$/;  # Qty
        next unless $row->[3] && $row->[3] =~ /^\$?[\d.]+$/;  # Unit price
        
        my $price = $row->[3];
        $price =~ s/^\$//;
        my $qty = $row->[4];
        $file_total += $price * $qty;
    }
    close $fh;
    
    ok($file_total > 0, "BOM has calculable total: $bom_file = \$$file_total");
    $total_cost += $file_total;
}

ok($total_cost < 500, "Total hardware cost under \$500: \$$total_cost");

print "\nHardware tests complete. Total BOM value: \$$total_cost\n";
