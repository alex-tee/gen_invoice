gen invoice
===========

`gen_invoice` is a pandoc invoice generator.

It creates invoices from a markdown-html template,
a YAML file containing client info, an address
file containing our address and a payment info
file containing our payment info.

# Usage

```
usage: gen-invoice.py [-h] [--items ITEM [ITEM ...]]
                      [--companies-file COMPANIES_FILE]
                      [--my-address-file MY_ADDRESS_FILE]
                      [--my-payment-info-file MY_PAYMENT_INFO_FILE]
                      ID COMPANY

positional arguments:
  ID                    invoice ID
  COMPANY               short company name

optional arguments:
  -h, --help            show this help message and exit
  --items ITEM [ITEM ...]
                        comma separated item (item,quantity,rate)
  --companies-file COMPANIES_FILE
                        companies yaml file to use
  --my-address-file MY_ADDRESS_FILE
                        html to show for our address
  --my-payment-info-file MY_PAYMENT_INFO_FILE
                        html to show for our payment info
```

# Example
```
./gen-invoice.py 1234 dummy --companies-file=example_companies.yaml --my-address-file=MY_DUMMY_ADDRESS.html --my-payment-info-file=MY_DUMMY_PAYMENT_INFO.html --items "abc,1,12.00" "second,4,23.21"
```

This will create the `example.pdf` file in this distribution.

# License
Copyright (C) 2019 Alexandros Theodotou

Licensed under the AGPLv3+. See the [COPYING](COPYING) file
for details.

----

Copyright (C) 2019 Alexandros Theodotou

Copying and distribution of this file, with or without modification,
are permitted in any medium without royalty provided the copyright
notice and this notice are preserved.  This file is offered as-is,
without any warranty.
