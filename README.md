# Requirements

* Make the last day configurable. If not specified, quickly detect it
* Have a flag to figure out the data types to ignore. The different types are real,bool.
* Make the file path configurable
* Make the output file path configurable

# End Goal

* Align the data points at 30 minute intervals. For environmental values this is pure sampling, For utility data this is summing.
* Go back 60 days from last day
* Eliminate the boolean values
* Apply the heuristic for the empty values (if needed)
* Transform the output to the schema you will provide tomorrow.
