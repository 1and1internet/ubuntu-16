require 'serverspec'
require 'docker'

#Include Tests
base_spec_dir = Pathname.new(File.join(File.dirname(__FILE__)))
Dir[base_spec_dir.join('../../drone-tests/shared/**/*.rb')].sort.each { |f| require_relative f }

if not ENV['IMAGE'] then
  puts "You must provide an IMAGE env variable"
end

RSpec.configure do |c|
  @image = Docker::Image.get(ENV['IMAGE'])
  set :backend, :docker
  set :docker_image, @image.id
#  set :docker_container_create_options, { 'User' => '100000', 'Hostname' => 'ubuntu_16', 'Env' => [ 'SUPERVISORD_EXIT_ON_FATAL=0' ] }
  set :docker_container_create_options, { 'User' => '100000' }

  describe "tests" do
    include_examples 'docker-ubuntu-16'
  end
end
