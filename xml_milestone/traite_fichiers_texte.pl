#!/usr/bin/perl -w

use strict;


my $comp_dir = 'milestone';

my @filesFC = `ls *xml`;


foreach my $file (@filesFC) {

	chop $file;

	my $txtfile = $file;
	$txtfile =~ s/\.xml$/.xml/;

	my $cmd = "xsltproc xml2xml_ajout-milestone.xsl $file > $txtfile";
	`$cmd`;
}
