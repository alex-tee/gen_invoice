---
papersize: a4
margin-left: 15mm
margin-right: 15mm
margin-top: 15mm
margin-bottom: 15mm
---

<p style="float:left">**@COMPANYNAME@**<br>@COMPANYINFO@</p>
<p style="float:right;text-align:right">**Alexandros Theodotou**<br>@MYADDRESS@</p>
<p style="clear:both;text-align:right"><br><b>Invoice No.: @INVOICEID@</b><br>Date: @DATE@</p>
<br>
<p style="text-align:center">Invoice for<br>**@COMPANYNAME@**</p>
<br>
<p>Description:</p>

- - -

<table style="padding:3px 3px">
  <colgroup>
     <col span="1" style="width: 60%;">
     <col span="1" style="width: 10%;">
     <col span="1" style="width: 15%;">
     <col span="1" style="width: 15%;">
  </colgroup>
  <thead>
    <th style="text-align:left">Item</th>
    <th>Quantity</th>
    <th style="text-align:right">Rate</th>
    <th style="text-align:right">Amount</th>
  </thead>
  <tbody>
  </tbody>
</table>

- - -

<br><p style="text-align:right">**Total Amount Due:<br>@TOTAL@ @CURRENCY@**</p>

<br><p>To be paid within @DAYSDUE@ days to:</p>
@MYPAYMENTINFO@

<!-- Originally authored by Milk Brewster. Modifications by
Alexandros Theodotou -->
