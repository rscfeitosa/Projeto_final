let varA = 'A';
let varB = 'B';
let varC = 'C';
let varD = '';

/*varD = varA;
varA = varB;
varB = varC;
varC = varD;*/

[varA,varB,varC] = [varB,varC,varA];


console.log(varA,varB,varC);