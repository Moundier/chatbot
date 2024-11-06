const cmds = new Map<string, string>();

cmds.set('/', `
Digite um numero:
1️⃣ Ver comandos do bot
2️⃣ Agendar uma consulta
3️⃣ Falar com atendente
4️⃣ Sugerir mudanca
5️⃣ Ver informacoes
`.trim());

cmds.set('/dev', `
Chatbot Information 🤖
🖥️ Execution Environment: local server
🚀 Version: 1.0.0
📅 Release Date: July 20th, 2024
🛠️ Platform: Node.js v21.x
🐧 Operating System: Arch Linux 20.04
👨‍💻 Developer: Gabriel Vieira Casanova
`.trim());

cmds.set('1', `
Comandos do Bot:
- /: Chame pelo chatbot
- /dev: Informações sobre o chatbot
- Outros comandos virão no futuro!
`.trim());

cmds.set('2', `
Por favor, forneça a data e hora desejadas para a consulta.
`.trim());

cmds.set('3', `
Conectando você com um atendente. Por favor, aguarde...
`.trim());

cmds.set('4', `
Por favor, digite sua sugestão abaixo:
`.trim());

cmds.set('5', `
Aqui estão mais informações sobre nossos serviços e suporte...
`.trim());

export default cmds;
