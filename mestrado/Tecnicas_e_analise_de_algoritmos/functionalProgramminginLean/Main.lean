structure Point where
  x : Float
  y : Float
deriving Repr

def origin : Point := {x := 0.0, y := 0.0}

#eval origin


def zeroX (p : Point) : Point :=
  { p with x := 0 }

#eval zeroX origin


structure PPoint (a : Type) (b : Type) where
  x : a
  y : b
deriving Repr

def f := PPoint.mk 1 1

#eval PPoint.mk 1 f
-- Define Digit as a subtype of Int for digits 0-9
def Digit := { n : Int // 0 ≤ n ∧ n < 10 }

-- Helper to create a Digit
def mkDigit (n : Int) (h : 0 ≤ n ∧ n < 10) : Digit := ⟨n, h⟩

-- Halve function: (n + 1) / 2
def halve (n : Int) : Int := (n + 1) / 2

-- Shift function for intern
def shiftn (d : Digit) (n : Int) : Int := (131072 * d.val + n) / 10

-- Intern: Convert list of digits to TEX internal representation
def intern (ds : List Digit) : Int :=
  halve (ds.take 17 |>.foldr shiftn 0)

-- Helper to generate a range of Int from l to u (inclusive)
def intRange (l u : Int) : List Int :=
  if l > u then []
  else List.range' l.toNat (u - l + 1).toNat |>.map Int.ofNat

-- Decimals: Generate all decimal fractions in the interval [a, b) for w = 131072
def decimals (w : Int) (a b : Int) (depth : Nat) : List (List Digit) :=
  if a ≤ 0 || depth = 0 then [[]]
  else
    let l := max 0 ((10 * a) / w)
    let u := min 9 ((10 * b) / w)
    intRange l u |>.flatMap (λ d =>
      if h : 0 ≤ d ∧ d < 10 then
        let d' := mkDigit d h
        (decimals w (10 * a - w * d) (10 * b - w * d) (depth - 1)).map (λ ds => d' :: ds)
      else [])
termination_by depth

-- Externs: Generate decimals for a given internal value n
def externs (n : Int) : List (List Digit) :=
  decimals 131072 (2 * n - 1) (2 * n + 1) 17

-- Lexical ordering for lists of digits
def lexicalLt (ds1 ds2 : List Digit) : Bool :=
  match ds1, ds2 with
  | [], [] => false
  | [], _ => true
  | _, [] => false
  | d1 :: ds1', d2 :: ds2' => if d1.val = d2.val then lexicalLt ds1' ds2' else d1.val < d2.val

-- Select the shortest and lexically largest decimal fraction
def maximumByLengthAndLex (dss : List (List Digit)) : Option (List Digit) :=
  dss.minimumBy (λ ds1 ds2 =>
    if ds1.length = ds2.length then lexicalLt ds2 ds1 else ds1.length < ds2.length)

-- Extern: Convert internal representation to the lexically largest shortest decimal
def extern (n : Int) : List Digit :=
  match maximumByLengthAndLex (externs n) with
  | some ds => ds
  | none => []