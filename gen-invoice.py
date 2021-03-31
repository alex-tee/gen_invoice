#!/usr/bin/env python3
#
#  Copyright (C) 2019 Alexandros Theodotou <alex at zrythm dot org>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

import fileinput
import subprocess
import yaml

from argparse import ArgumentParser
from datetime import datetime

# replace the placeholders in the file using the
# given dictionary and place the results in a new file
# filename + .tmp
def replace_placeholders(filename, dictionary):
    fin = open(filename, "r")
    with open(filename + ".tmp", "w") as fout:
        for line in fin.readlines():
            for word in dictionary.keys():
                line = line.replace(word, switch[word])
            fout.write(line)
    fin.close()

# finds the company object from the companies file based
# on the short name
def find_company(name):
    with open(args.companies_file[0]) as f:
        yaml_info = yaml.safe_load(f)
        for company in yaml_info:
            if company['shortname'] == name: return company

# returns a string with 2 decimal points from
# the given float
def float_to_string(num,n_decimals):
    fmt = '{:,.' + str(n_decimals) + 'f}'
    return fmt.format(num)

# inserts the given text at the given line number
# in the given file
def insert_at_line(filename,lineno,txt):
    f = open(filename, "r")
    contents = f.readlines()
    f.close()
    contents.insert(lineno, txt)
    f = open(filename, "w")
    contents = "".join(contents)
    f.write(contents)
    f.close()

# replaces a string inline in the given file
def replace_in_file(filename,take,put):
    UserFile = open(filename, 'r+')
    UserFileT = open(filename, 'r+')
    for line in UserFile:
        UserFileT.write(line.replace(take,put))
    UserFile.close()
    UserFileT.close()

orig_file = "invoice-template.md"
tmp_file = orig_file + '.tmp'

# parse arguments
parser = ArgumentParser()
parser.add_argument(
    "invoice_id", metavar="ID",
    nargs=1, help="invoice ID")
parser.add_argument(
    "company", metavar="COMPANY",
    nargs=1, help="short company name")
parser.add_argument(
    "--items", metavar="ITEM",
    nargs='+',
    help="comma separated item (item,quantity,rate)")
parser.add_argument(
    "--companies-file", default=["companies.yaml"],
    nargs=1, help="companies yaml file to use")
parser.add_argument(
    "--my-address-file", default=["MY_ADDRESS.html"],
    nargs=1, help="html to show for our address")
parser.add_argument(
    "--my-payment-info-file",
    default=["MY_PAYMENT_INFO.html"],
    nargs=1, help="html to show for our payment info")
parser.add_argument(
    "--currency", metavar="CURRENCY",
    nargs='?', default=None,
    help="override currency specification")

args = parser.parse_args()

# get company, invoice id, current date, currency
company = find_company(args.company[0])
print('found {}'.format(company['fullname']))
invoice_id = args.invoice_id[0]
curr_date = datetime.today().strftime('%Y-%m-%d')
if args.currency is None:
    currency = company['currency']
else:
    currency = args.currency

# create the tmp template by replacing some placeholders
switch = {
    "@DATE@": curr_date,
    "@COMPANYNAME@": company['fullname'],
    "@COMPANYINFO@": company['info'].replace('\n','<br>'),
    "@INVOICEID@": invoice_id,
    "@CURRENCY@": currency,
    "@DAYSDUE@": str(company['daysdue']),
    }
replace_placeholders(orig_file, switch)
print('replaced placeholders')

# insert the items in the tmp template
total = 0.00
for item in reversed(args.items):
    items = item.split(',')
    descr = items[0]
    qty = int(items[1])
    rate = float(items[2])
    value = """<tr>
<td>{}</td>
<td style="text-align:center">{}</td>
<td style="text-align:right">{}</td>
<td style="text-align:right">{}</td>
</tr>""".format(
        descr, qty, float_to_string(rate, 3),
        float_to_string (qty * rate, 2))
    # insert at line 32
    insert_at_line(tmp_file, 32, value)
    total += qty * rate

# replace the total
replace_in_file(
    tmp_file, '@TOTAL@', float_to_string(total, 2))

# replace the address and payment info
my_address = ''
with open(args.my_address_file[0], 'r') as content_file:
    my_address = content_file.read()
replace_in_file(
    tmp_file, '@MYADDRESS@', my_address)
my_payment_info = ''
with open(args.my_payment_info_file[0], 'r') as content_file:
    my_payment_info = content_file.read()
replace_in_file(
    tmp_file, '@MYPAYMENTINFO@', my_payment_info)

# compile invoice pdf, saving to a
# file called <invoice ID>_<company short name>_<date>
date_for_filename = datetime.today().strftime('%d-%m-%Y')
subprocess.run([
    'pandoc', '-t', 'html5', '--metadata',
    'pagetitle="Invoice {} from Alexandros Theodotou"'.format(invoice_id),
    '--css', 'style.css', '-o',
    '{}_{}_{}.pdf'.format(invoice_id, company['shortname'], date_for_filename),
    'invoice-template.md.tmp',
    ])
