# Typesense fast index tool evaluation

TS showed much promise initially and the test resource (9K records) seemed really neet.
**However** when applied to a 1.2M records table, the TS results were inconsistent with the Postgres table from which the export came from.
The number of hits for specific names did not match the database count operation. In this context, the Postgres DB table is the ground truth.
 
The TS version tested was 0.22 and I cannot recommend this product as it is currently. 
