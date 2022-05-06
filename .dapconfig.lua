require'dap'.configurations.python = {
  {
    type = 'python',
    request = 'launch',
    name = 'Launch file',
    program = '${workspaceFolder}/main.py',
    cwd = '${workspaceFolder}',
    args = {}
}}
