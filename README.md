# CSTORE_FDW 1.4 RPM built for RHEL 6.5

**Description**: 

This extension implements a columnar store for PostgreSQL. 
Columnar stores provide notable benefits for analytic use-cases where data is loaded in batches.

This extension implements a columnar store for PostgreSQL. Columnar stores
provide notable benefits for analytic use-cases where data is loaded in batches.

Join the [Mailing List][mailing-list] to stay on top of the latest developments.

## Dependencies

cstore\_fdw depends on protobuf-c for serializing and deserializing table metadata.
So we need to install these packages first:

    # Fedora 17+, CentOS, and Amazon Linux
    sudo yum install protobuf-c-devel

**Note.** In CentOS 5 and 6, you may need to install or update EPEL 5 or EPEL 6
repositories. See [this page]
(http://www.rackspace.com/knowledge_center/article/installing-rhel-epel-repo-on-centos-5x-or-6x)
for instructions.

**Note.** In Amazon Linux, EPEL 6 repository is installed by default, but it is not 
enabled. See [these instructions](http://aws.amazon.com/amazon-linux-ami/faqs/#epel)
for how to enable it. 

**Note.** cstore_fdw requires PostgreSQL 9.3, 9.4 or 9.5. It doesn't support earlier
versions of PostgreSQL.


## Installation

Build RPM using Vagrant

    1. The repo is cloned into a local sandbox
    2. Run "vagrant up" to build the VM. 
    3. Run "vagrant ssh" to connect to VM. 
    4. Run rpmbuild -ba SPECS/cstore.spec --define 'pg_dir /usr/pgsql-9.4'  to build the cstore rpm package.

    Please note: "pg_dir" must be available in your environment path

Build RPM on server

    1. Once repo is cloned, run "sh ./bootstrap.sh"
    2. cd to ~/rpmbuild 
    3. Run the following command 
      rpmbuild -ba /SPECS/cstore.spec  --define 'pg_dir /usr/pgsql-9.4'

    Please note that "pg_dir" MUST be accessible in users path...

## Installing the RPM 

    Install the built RPM by running "sudo yum install RPMS/x86_64/cstore-1.4-1.el6.x86_64.rpm"


Introduction
------------

This extension uses the Optimized Row Columnar (ORC) format for its data layout.
ORC improves upon the RCFile format developed at Facebook, and brings the
following benefits:

* Compression: Reduces in-memory and on-disk data size by 2-4x. Can be extended
  to support different codecs.
* Column projections: Only reads column data relevant to the query. Improves
  performance for I/O bound queries.
* Skip indexes: Stores min/max statistics for row groups, and uses them to skip
  over unrelated rows.

Further, we used the Postgres foreign data wrapper APIs and type representations
with this extension. This brings:

* Support for 40+ Postgres data types. The user can also create new types and
  use them.
* Statistics collection. PostgreSQL's query optimizer uses these stats to
  evaluate different query plans and pick the best one.
* Simple setup. Create foreign table and copy data. Run SQL.



Usage
-----

Before using cstore\_fdw, you need to add it to ```shared_preload_libraries```
in your ```postgresql.conf``` and restart Postgres:

    shared_preload_libraries = 'cstore_fdw'    # (change requires restart)

The following parameters can be set on a cstore foreign table object.

* filename (optional): The absolute path to the location for storing table data.
  If you don't specify the filename option, cstore\_fdw will automatically
  choose the $PGDATA/cstore\_fdw directory to store the files. If specified the 
  value of this parameter will be used as a prefix for all files created to
  store table data. For example, the value ```/cstore_fdw/my_table``` could result in
  the files ```/cstore_fdw/my_table``` and ```/cstore_fdw/my_table.footer``` being used
  to manage table data.
* compression (optional): The compression used for compressing value streams.
  Valid options are ```none``` and ```pglz```. The default is ```none```.
* stripe\_row\_count (optional): Number of rows per stripe. The default is
  ```150000```. Reducing this decreases the amount memory used for loading data
  and querying, but also decreases the performance.
* block\_row\_count (optional): Number of rows per column block. The default is
 ```10000```. cstore\_fdw compresses, creates skip indexes, and reads from disk
  at the block granularity. Increasing this value helps with compression and results
  in fewer reads from disk. However, higher values also reduce the probability of
  skipping over unrelated row blocks.


To load or append data into a cstore table, you have two options:

* You can use the [```COPY``` command][copy-command] to load or append data from
  a file, a program, or STDIN.
* You can use the ```INSERT INTO cstore_table SELECT ...``` syntax to load or
  append data from another table.

You can use the [```ANALYZE``` command][analyze-command] to collect statistics
about the table. These statistics help the query planner to help determine the
most efficient execution plan for each query.

**Note.** We currently don't support updating table using DELETE, and UPDATE
commands. We also don't support single row inserts.


Updating from earlier versions to 1.4
--------------------------------------

To update your existing cstore_fdw installation from earlier versions 1.4 
you can take the following steps:

* Download and install cstore_fdw version 1.4 using instructions from the "Building"
  section,
* Restart the PostgreSQL server,
* Run the ```ALTER EXTENSION cstore_fdw UPDATE;``` command.


Example
-------

As an example, we demonstrate loading and querying data to/from a column store
table from scratch here. Let's start with downloading and decompressing the data
files.

    wget http://examples.citusdata.com/customer_reviews_1998.csv.gz
    wget http://examples.citusdata.com/customer_reviews_1999.csv.gz

    gzip -d customer_reviews_1998.csv.gz
    gzip -d customer_reviews_1999.csv.gz

Then, let's log into Postgres, and run the following commands to create a column
store foreign table:

```SQL
-- load extension first time after install
CREATE EXTENSION cstore_fdw;

-- create server object
CREATE SERVER cstore_server FOREIGN DATA WRAPPER cstore_fdw;

-- create foreign table
CREATE FOREIGN TABLE customer_reviews
(
    customer_id TEXT,
    review_date DATE,
    review_rating INTEGER,
    review_votes INTEGER,
    review_helpful_votes INTEGER,
    product_id CHAR(10),
    product_title TEXT,
    product_sales_rank BIGINT,
    product_group TEXT,
    product_category TEXT,
    product_subcategory TEXT,
    similar_product_ids CHAR(10)[]
)
SERVER cstore_server
OPTIONS(compression 'pglz');
```

Next, we load data into the table:

```SQL
COPY customer_reviews FROM '/home/user/customer_reviews_1998.csv' WITH CSV;
COPY customer_reviews FROM '/home/user/customer_reviews_1999.csv' WITH CSV;
```

**Note.** If you are getting ```ERROR: cannot copy to foreign table
"customer_reviews"``` when trying to run the COPY commands, double check that you
have added cstore\_fdw to ```shared_preload_libraries``` in ```postgresql.conf```
and restarted Postgres.

Next, we collect data distribution statistics about the table. This is optional,
but usually very helpful:

```SQL
ANALYZE customer_reviews;
```

Finally, let's run some example SQL queries on the column store table.

```SQL
-- Find all reviews a particular customer made on the Dune series in 1998.
SELECT
    customer_id, review_date, review_rating, product_id, product_title
FROM
    customer_reviews
WHERE
    customer_id ='A27T7HVDXA3K2A' AND
    product_title LIKE '%Dune%' AND
    review_date >= '1998-01-01' AND
    review_date <= '1998-12-31';

-- Do we have a correlation between a book's title's length and its review ratings?
SELECT
    width_bucket(length(product_title), 1, 50, 5) title_length_bucket,
    round(avg(review_rating), 2) AS review_average,
    count(*)
FROM
   customer_reviews
WHERE
    product_group = 'Book'
GROUP BY
    title_length_bucket
ORDER BY
    title_length_bucket;
```


Usage with CitusDB
--------------------

The example above illustrated how to load data into a PostgreSQL database running
on a single host. However, sometimes your data is too large to analyze effectively
on a single host. CitusDB is a product built by Citus Data that allows you to run
a distributed PostgreSQL database to analyze your data using the power of multiple
hosts. CitusDB is based on a modern PostgreSQL version and allows you to easily
install PostgreSQL extensions and foreign data wrappers, including cstore_fdw. For
an example of how to use cstore\_fdw with CitusDB see the
[CitusDB documentation][citus-cstore-docs].


Using Skip Indexes
------------------

cstore_fdw partitions each column into multiple blocks. Skip indexes store minimum
and maximum values for each of these blocks. While scanning the table, if min/max
values of the block contradict the WHERE clause, then the block is completely
skipped. This way, the query processes less data and hence finishes faster.

To use skip indexes more efficiently, you should load the data after sorting it
on a column that is commonly used in the WHERE clause. This ensures that there is
a minimum overlap between blocks and the chance of them being skipped is higher.

In practice, the data generally has an inherent dimension (for example a time field)
on which it is naturally sorted. Usually, the queries also have a filter clause on
that column (for example you want to query only the last week's data), and hence you
don't need to sort the data in such cases.


## Getting help

For all types of questions and comments about the wrapper, please contact 
engage @ citusdata.com.

## Other helpful links
[status]: https://travis-ci.org/citusdata/cstore_fdw
[mailing-list]: https://groups.google.com/forum/#!forum/cstore-users
[citus-cstore-docs]: https://www.citusdata.com/documentation/citusdb-documentation/
[coverage]: https://coveralls.io/r/citusdata/cstore_fdw
[copy-command]: http://www.postgresql.org/docs/current/static/sql-copy.html
[analyze-command]: http://www.postgresql.org/docs/current/static/sql-analyze.html

## Open source licensing info
1. [TERMS](TERMS.md)
2. [LICENSE](LICENSE)
3. [CFPB Source Code Policy](https://github.com/cfpb/source-code-policy/)


