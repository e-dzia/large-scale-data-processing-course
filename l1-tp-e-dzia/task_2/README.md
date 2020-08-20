# L1 - 2019

## Task 2
Proof that you can use Vim:
- find an expression
  ```text
  Answer: ?<word_to_find> or /<word_to_find> then press 'n' to find next occurence
  ```
- jump to line
  ```text
  Answer: :<line_number>
  ```
- substitute a single character
  ```text
  Answer: r<character_to_substitute> (works for current position of cursor and for one occurence only)
  ```
- substitute a whole expression
  ```text
  Answer: :s/foo/bar/g reaplces all foo in current line with bar
  :%s/foo/bar/g replaces all foo with bar in the whole file
  ```
- save changes
  ```text
  Answer: :w
  ```
- exit Vim (2 ways)
  ```text
  Answer: :q! (without save) or :wq (with save) or Shift ZQ (without save) or Shift ZZ (with save)
   ```
- go back to write mode
 ```text
  Answer: Esc + i
  ```
