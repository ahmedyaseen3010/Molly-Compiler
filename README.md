# Molly-Compiler
<h2>Grammer</h2>
<p>
  <ul>
    <li>  program -> statement | statement program
</li>
    <li>	statement -> assignment | expression
</li>
    <li>	assignment -> "letvar" identifier '=' expression
</li>
    <li>	letvar -> "letvar"
</li>
    <li>	expression -> term | term op expression
</li>
    <li>	term -> identifier | number | '(' expression ')'
</li>
    <li>	op -> '+' | '-' | '*' | '/'
</li>
    <li>	identifier -> letter | digit | identifier letter | identifier digit
</li>
    <li>	number -> digit | number digit
</li>
    <li>	letter -> 'a' | 'b' | 'c' |...| 'z' |
</li>
    <li>	digit -> '0' | '1' | '2' | '3' | '4' |...| '99'
</li>
  </ul>
</p>
<img src="https://github.com/ahmedyaseen3010/Molly-Compiler/assets/87431777/5ae02a7c-374b-4877-87c7-c67e2f9c844c">
