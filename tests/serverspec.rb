require "serverspec"
require "docker"

#Include Tests
base_spec_dir = Pathname.new(File.join(File.dirname(__FILE__)))
Dir[base_spec_dir.join('../drone-tests/shared/**/*.rb')].sort.each{ |f| require_relative f }

describe "Dockerfile" do
  before(:all) do
    @image = Docker::Image.get(ENV['IMAGE'])

    set :backend, :docker
    set :docker_image, @image.id
    set :docker_container_create_options, { 'User' => '100000' }
  end

  #Add include statements here including tests from shared repo
  include_examples 'docker-ubuntu-16'
end
