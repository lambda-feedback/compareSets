# compareSets
### Overview
Checks if a student's set expression matches the correct answer. Can compare both the meaning and exact form of set expressions.  
Can also compare sets written in set notation containing elements, to see if the elements are the same.
When to Use  
For questions involving set operations like union (∪), intersection (∩), and complement.  

### Syntax
  
|Operator|Meaning  |LaTeX         |
|--------|---------|--------------|
|`A u B` or `A \cup B`|`A union B` |$A \cup B$       |
|`A n B` or `A \cap B` |`A intersection B`|$A \cap B$   |
|`A'`    |`A complement`  |$A^c$|

### Examples:

"Express the union of sets A and B"  
"Simplify: (A ∪ B) ∩ C"  
"Write the positive integers less than 5 in set notation"

### Parameters
`is_latex` (optional)

Default: `false`  
Description: Set to true if students enter answers in LaTeX format (\cup, \cap). Set to false for plain text.

`enforce_expression_equality` (optional)

Default: `false`  
Description:

`false`: Accepts any mathematically equivalent form (e.g., "A ∪ B" = "B ∪ A")
`true`: Requires exact form match

`is_set_notation` (optional)

Default: `false`  
Description: Set to true if students enter a response in set notation, e.g. `{1,2}`. Set to false if responses are named sets, e.g. `A n B`.
