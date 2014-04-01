require 'sinatra'

set :environment, :production
set :raise_exceptions, :false


def render_me(page_view, script='none')
  haml page_view, :format => :html5, :locals => {:jsscript => script}
end

def render_mp(n)
  mpn = "mp#{n}"
  render_me mpn.to_sym, mpn
end

get '/' do
  render_me :home, 'none'
end

get '/mp1' do
  render_mp 1
end

get '/mp2' do
  render_mp 2
end

get '/mp3' do
  render_mp 3
end

error do
  status 400
  render_me :wut
end

not_found do
  status 404
  render_me :wut
end
