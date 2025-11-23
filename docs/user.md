# compareSets
### Overview
Checks if a student's set expression matches the correct answer. Can compare both the meaning and exact form of set expressions.
When to Use
For questions involving set operations like union (∪), intersection (∩), and complement.

### Examples:

"Express the union of sets A and B"
"Simplify: (A ∪ B) ∩ C"

Parameters
`is_latex` (optional)

Default: `false`
Description: Set to true if students enter answers in LaTeX format (\cup, \cap). Set to false for plain text.

`enforce_expression_equality` (optional)

Default: `false`
Description:

`false`: Accepts any mathematically equivalent form (e.g., "A ∪ B" = "B ∪ A")
`true`: Requires exact form match
