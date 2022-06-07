mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"m.celina.bermudez@gmail.com\"\n\
" > ~/.streamlit/config.toml

echo "\
[server]\n\
hardless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
