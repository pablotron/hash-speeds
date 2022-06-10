# frozen_string_literal: true

require 'rubocop/rake_task'

# FIXME: move to rubocop config
EXCEPT_COPS = %w{
  Layout/FirstHashElementIndentation
  Layout/FirstHashElementIndentation
  Layout/SpaceAroundOperators
  Style/TrailingCommaInHashLiteral
}

# define rubocop task
RuboCop::RakeTask.new(:rubocop) do |t|
  t.options = ['--except', EXCEPT_COPS.join(','), 'bin/bench.rb']
end
