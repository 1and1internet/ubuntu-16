require "serverspec"
require "docker"

#Include Tests
base_spec_dir = Pathname.new(File.join(File.dirname(__FILE__)))
Dir[base_spec_dir.join('drone-tests/shared/**/*.rb')].sort.each{ |f| require_relative f }

# THIS ISN'T WORKING FOR SOME REASON
describe "Dockerfile env test" do
  before(:all) do
    @image = Docker::Image.get(ENV['IMAGE'])

    set :backend, :docker
    set :docker_image, @image.id
    set :docker_container_create_options, { 'User' => '100000' }
    @image.json['ContainerConfig']['Env'] << 'SUPERVISORD_EXIT_ON_FATAL=0'
    #set :env, 'SUPERVISORD_EXIT_ON_FATAL=0'
  end

  describe 'check env vars' do
    it 'supervisord_exit_on_fatal something' do
      expect(@image.json).to include("bob")
    end
  end

#  describe command('echo $SUPERVISORD_EXIT_ON_FATAL') do
#    its(:stdout) { should match /^0$/ }
#  end

  describe "Container" do
    before(:all)  do
      @container = Docker::Container.create(
        'Image'        => @image.id,
        'HostConfig'   => {
          'PortBindings' => { "#{LISTEN_PORT}/tcp" => [{ 'HostPort' => "#{LISTEN_PORT}" }]},
        },
        'Env'          => [ 'SUPERVISORD_EXIT_ON_FATAL=0' ],
      )
      @container.start
    end

    describe command("echo $SUPERVISORD_EXIT_ON_FATAL") do
      its(:stdout) { should match /^0$/ }
    end

    after(:all) do
      @container.kill
      @container.delete(:force => true)
    end
  end


end


