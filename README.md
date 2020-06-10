# AutodeskFlexLicenseParser
Script parses the FLEXLM log file to collect usage and inserts into MySQL database.

At the time of writing this, we were interested in going with an enterprise license; therefore, the code 
will count a maximum of one checkout per product per user a day. This could be changed by removing the 
"ignore" from the SQL query.

