require 'sinatra'

set :environment, :production
set :raise_exceptions, :false


def render_me(page_view, script='none')
  haml page_view, :format => :html5, :locals => {:jsscript => script}
end

get '/' do
  render_me :home, 'none'
end

get '/mp1' do
  render_me :mp, 'mp1'
end

get '/error' do
  status 404
  render_me :wut
end

error do
  status 400
  render_me :wut
end

not_found do
  status 404
  render_me :wut
end
