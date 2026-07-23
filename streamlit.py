python -c "
with open('.streamlit/config.toml', 'w') as f:
    f.write('''[server]
headless = true
port = 8501
enableCORS = false

[theme]
base = \"dark\"
primaryColor = \"#e24b4a\"
backgroundColor = \"#0d1117\"
secondaryBackgroundColor = \"#161b22\"
textColor = \"#e6edf3\"
font = \"monospace\"
''')
print('config.toml criado')
"