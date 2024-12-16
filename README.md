# Sales_Numbers
### A simple way of compiling and emailing sales data from multiple retail stores.

Sales_Numbers was built mostly as a "I wonder if I could build this" type project - the task carried out by this program is normally done semi manually using Google Forms at my company - and I figured having it fully automated could save a lot of headaches.

### So, what does it do?

Sales_Numbers carries out the following functions:

1. Runs a simple website that stores enter their sales data into, where they are stored in a database.
2. Checks an email inbox daily for an email containing a specific Excel spreadsheet, and parses it's budget data.
3. At a set time (configurable in the `crontab` file), the web app compiles these datapoints into a HTML table, which is then emailed to all the stores. 

The entire program is built to be run in a Docker container for portability. 
