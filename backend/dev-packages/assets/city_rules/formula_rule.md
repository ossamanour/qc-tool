### Rule to write the formula in the csv files.

#### Common rule:

1. All math symbols: `+`, `-`, `*`, `/`, `(`, `)`, MUST have space on both side. This is to distinguish it from possible symbols in the parameter description.

#### Condition case:

1. For cases in which different formulas are used under different conditions, use the following statement:
   `condition ? statement_yes : statement_no`
2. Both `:` and `?` MUST have space on both side.

#### `min()` / `max()` command:

1. Right now, the function `eval()` only support simple `min()` / `max()` string which contains only the `min()` / `max()`. For such cases, the rule to write the formula is
   `MIN statement1 : statement2`

   `MAX statement1 : statement2`

2. THe whole command must start with `MIN` or `MAX`.
3. `MIN` / `MAX` MUST be capital without `()` and `:` MUST have space on both side.
4. `statement1` and `statement2` can be either naive number or basic statemetn follow _Common rule 1_.
