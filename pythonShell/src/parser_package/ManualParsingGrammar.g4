grammar ManualParsingGrammar;
parse: statement+ EOF;

pipeStatement: WS* (callStatement|(substitutionStatement)) WS* PIPE WS* (callStatement|(app WS* substitutionStatement)) WS* (PIPE callStatement|(app WS* substitutionStatement))*;

callStatement: WS* app WS* args? WS*;

args: (string WS*)+;
argsForSub: (string WS*)+;

substitutionStatement: WS* app args? (WS* SUBSTITUTION WS* statement WS* SUBSTITUTION ) argsForSub?;

statement: (callStatement | pipeStatement | substitutionStatement);

app: 'echo' | 'pwd' | 'cd' | 'head' | 'cat' | 'ls' | 'tail' | 'grep'| 'sort' | 'cut' | 'find' | 'uniq' | '_echo' | '_pwd' | '_cd' | '_head' | '_cat' | '_ls' | '_tail' | '_grep'| '_sort' | '_cut' | '_find' | '_uniq';

fileName: WS* string WS*;

string: NON_QUOTE+ | DOUBLE_QUOTE_STRING | SINGLE_QUOTE_STRING| SPACE;

DOUBLE_QUOTE_STRING: '"' (NON_QUOTE | ESCAPED_QUOTE)* '"';
SINGLE_QUOTE_STRING: '\'' (NON_QUOTE | ESCAPED_QUOTE)* '\'';

SPACE: ' ';
NON_QUOTE: ~['`|];
ESCAPED_QUOTE: '\\"';
PIPE: '|';
SUBSTITUTION: '`';

WS: [\t\r\n]+ -> skip;

