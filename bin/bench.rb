#!/usr/bin/env ruby
# frozen_string_literal: true

#
# bench.rb: Generate hash benchmarks using `openssl speed` and write
# them to standard output as JSON.
#
# The output of this command should be fed into bin/plot.py to generate
# an SVG chart of the results.
#
# Note to self: use the following command to benchmark the compiled
# version of OpenSSL 3.0.3:
#
#   # generate stats
#   SSL_DIR=$HOME/src/openssl-3.0.3
#   export LD_LIBRARY_PATH="$SSL_DIR" PATH="$SSL_DIR/apps:$PATH"
#   bundle exec bin/bench.rb > data/flex-0.json
#

# load libraries
require 'json'
require 'time'
require 'yaml'

# load config.yaml
CONFIG = YAML.load_file(File.join(__dir__, 'config.yaml')).freeze

#
# Convert string representing bytes/sec to integer MB/s.
#
def to_mbs(val)
  (val.to_f / (2 ** 20)).floor
end

#
# Convert +F lines from output of `openssl speed -mr` to array of
# integers representing MB/s.
#
def to_data(line)
  line.strip.split(/:/)[3..].map { |s| to_mbs(s) }
end

# write as json to stdout
puts JSON({
  time: Time.now.gmtime.iso8601,

  # get cpu details
  lscpu: JSON(IO.popen(CONFIG['bench']['commands']['lscpu']).read),

  # get openssl version details
  openssl: IO.popen(CONFIG['bench']['commands']['openssl']).read,

  # run benchmarks, parse results
  results: CONFIG['bench']['hashes'].map do |hash|
    # log hash ID
    warn hash['id']

    # build benchmark command
    cmd = CONFIG['bench']['commands']['bench'] + [hash['id']]

    # run benchmark command, parse result
    IO.popen(cmd, err: %i[child out]) do |io|
      data = to_data(io.readlines.select { |s| s =~ /^\+F:/ }.first)
      { id: hash['id'], name: hash['name'], data: data }
    end
  end,
})
