const commands = new Map<string, string>();

commands.set('/', `
Digite um numero:
1️⃣ Ver comandos do bot
2️⃣ Agendar uma consulta
3️⃣ Falar com atendente
4️⃣ Sugerir mudanca
5️⃣ Ver informacoes
`.trim());

commands.set('/dev', `
Chatbot Information 🤖
🖥️ Execution Environment: local server
🚀 Version: 1.0.0
📅 Release Date: July 20th, 2024
🛠️ Platform: Node.js v21.x
🐧 Operating System: Arch Linux 20.04
👨‍💻 Developer: Gabriel Vieira Casanova
`.trim());

commands.set('1', `
Comandos do Bot:
- /: Chame pelo chatbot
- /dev: Informações sobre o chatbot
- Outros comandos virão no futuro!
`.trim());

commands.set('2', `Por favor, forneça a data e hora desejadas para a consulta.`.trim());

commands.set('3', `Conectando você com um atendente. Por favor, aguarde...`.trim());

commands.set('4', `Por favor, digite sua sugestão abaixo:`.trim());

commands.set('5', `Aqui estão mais informações sobre nossos serviços e suporte...`.trim());

export default commands;
