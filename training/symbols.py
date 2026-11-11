"""Display metadata for the HWRT symbols: a Unicode rendering and the LaTeX
package (if any) that provides the command. Used by export.py to build the
label table the web app shows; recognition itself does not depend on it."""

AMSSYMB = "amssymb"

_GREEK = {
    r"\alpha": "α", r"\beta": "β", r"\gamma": "γ", r"\Gamma": "Γ", r"\delta": "δ",
    r"\Delta": "Δ", r"\zeta": "ζ", r"\eta": "η", r"\theta": "θ", r"\Theta": "Θ",
    r"\vartheta": "ϑ", r"\epsilon": "ϵ", r"\varepsilon": "ε", r"\iota": "ι",
    r"\kappa": "κ", r"\varkappa": "ϰ", r"\lambda": "λ", r"\Lambda": "Λ", r"\mu": "μ",
    r"\nu": "ν", r"\xi": "ξ", r"\Xi": "Ξ", r"\pi": "π", r"\varpi": "ϖ", r"\Pi": "Π",
    r"\rho": "ρ", r"\varrho": "ϱ", r"\sigma": "σ", r"\Sigma": "Σ", r"\tau": "τ",
    r"\phi": "ϕ", r"\Phi": "Φ", r"\varphi": "φ", r"\chi": "χ", r"\psi": "ψ",
    r"\Psi": "Ψ", r"\omega": "ω", r"\Omega": "Ω",
}

_SYMBOLS = {
    # operators and big operators
    r"\sum": "∑", r"\prod": "∏", r"\coprod": "∐", r"\int": "∫", r"\oint": "∮",
    r"\partial": "∂", r"\cdot": "⋅", r"\pm": "±", r"\mp": "∓", r"\times": "×",
    r"\div": "÷", r"\ast": "∗", r"\star": "⋆", r"\circ": "∘", r"\bullet": "∙",
    r"\setminus": "∖", r"\cup": "∪", r"\cap": "∩", r"\uplus": "⊎", r"\sqcap": "⊓",
    r"\sqcup": "⊔", r"\vee": "∨", r"\wedge": "∧", r"\oplus": "⊕", r"\ominus": "⊖",
    r"\otimes": "⊗", r"\odot": "⊙", r"\amalg": "⨿", r"\wr": "≀", r"\diamond": "⋄",
    r"\triangleleft": "◁", r"\triangleright": "▷", r"\sqrt{}": "√", "-": "−",
    # relations
    r"\leq": "≤", r"\geq": "≥", r"\subset": "⊂", r"\supset": "⊃", r"\subseteq": "⊆",
    r"\supseteq": "⊇", r"\cong": "≅", r"\propto": "∝", r"\approx": "≈",
    r"\equiv": "≡", r"\not\equiv": "≢", r"\perp": "⊥", r"\asymp": "≍",
    r"\frown": "⌢", r"\prec": "≺", r"\succ": "≻", r"\bowtie": "⋈", r"\preceq": "⪯",
    r"\succeq": "⪰", r"\mid": "∣", r"\vdash": "⊢", r"\dashv": "⊣", r"\models": "⊨",
    r"\sim": "∼", r"\doteq": "≐", r"\parallel": "∥", r"\simeq": "≃", r"\neq": "≠",
    r"\sqsubseteq": "⊑", r"\in": "∈", r"\notin": "∉", r"\ni": "∋",
    # arrows
    r"\rightarrow": "→", r"\leftarrow": "←", r"\uparrow": "↑", r"\downarrow": "↓",
    r"\Rightarrow": "⇒", r"\Leftarrow": "⇐", r"\Downarrow": "⇓",
    r"\Leftrightarrow": "⇔", r"\leftrightarrow": "↔", r"\Longrightarrow": "⟹",
    r"\Longleftrightarrow": "⟺", r"\longrightarrow": "⟶", r"\longmapsto": "⟼",
    r"\mapsto": "↦", r"\hookrightarrow": "↪", r"\nearrow": "↗", r"\searrow": "↘",
    r"\rightleftharpoons": "⇌", r"\rightharpoonup": "⇀",
    # letter-like and misc
    r"\forall": "∀", r"\exists": "∃", r"\bot": "⊥", r"\top": "⊤", r"\ell": "ℓ",
    r"\hbar": "ℏ", r"\wp": "℘", r"\Im": "ℑ", r"\Re": "ℜ", r"\aleph": "ℵ",
    r"\infty": "∞", r"\prime": "′", r"\angle": "∠", r"\nabla": "∇",
    r"\emptyset": "∅", r"\neg": "¬", r"\triangle": "△", r"\backslash": "\\",
    r"\diamondsuit": "♢", r"\clubsuit": "♣", r"\heartsuit": "♡", r"\sharp": "♯",
    r"\flat": "♭", r"\dots": "…", r"\vdots": "⋮", r"\ddots": "⋱",
    r"\langle": "⟨", r"\rangle": "⟩", r"\lceil": "⌈", r"\rceil": "⌉",
    r"\lfloor": "⌊", r"\rfloor": "⌋", r"\|": "‖", r"\{": "{", r"\}": "}",
    r"\$": "$", r"\&": "&", r"\#": "#", r"\%": "%", r"\S": "§", r"\dag": "†",
    r"\pounds": "£", r"\copyright": "©", r"\mathcal{A}": "𝒜", r"\mathcal{B}": "ℬ",
    r"\mathcal{C}": "𝒞", r"\mathcal{D}": "𝒟", r"\mathcal{E}": "ℰ",
    r"\mathcal{F}": "ℱ", r"\mathcal{G}": "𝒢", r"\mathcal{H}": "ℋ",
    r"\mathcal{L}": "ℒ", r"\mathcal{M}": "ℳ", r"\mathcal{N}": "𝒩",
    r"\mathcal{O}": "𝒪", r"\mathcal{P}": "𝒫", r"\mathcal{R}": "ℛ",
    r"\mathcal{S}": "𝒮", r"\mathcal{T}": "𝒯", r"\mathcal{U}": "𝒰",
    r"\mathcal{X}": "𝒳", r"\mathcal{Z}": "𝒵",
    # text-mode letters
    r"\ss": "ß", r"\aa": "å", r"\AA": "Å", r"\L": "Ł", r"\O": "Ø", r"\o": "ø",
    r"\ae": "æ", r"\AE": "Æ", r"\guillemotleft": "«",
}

# (unicode, package)
_PACKAGED = {
    # amssymb
    r"\checkmark": ("✓", AMSSYMB), r"\circledR": ("®", AMSSYMB),
    r"\barwedge": ("⊼", AMSSYMB), r"\circledcirc": ("⊚", AMSSYMB),
    r"\boxdot": ("⊡", AMSSYMB), r"\boxplus": ("⊞", AMSSYMB),
    r"\boxtimes": ("⊠", AMSSYMB), r"\ltimes": ("⋉", AMSSYMB),
    r"\rtimes": ("⋊", AMSSYMB), r"\circledast": ("⊛", AMSSYMB),
    r"\lhd": ("⊲", AMSSYMB), r"\multimap": ("⊸", AMSSYMB),
    r"\pitchfork": ("⋔", AMSSYMB), r"\therefore": ("∴", AMSSYMB),
    r"\because": ("∵", AMSSYMB), r"\between": ("≬", AMSSYMB),
    r"\preccurlyeq": ("≼", AMSSYMB), r"\varpropto": ("∝", AMSSYMB),
    r"\Vdash": ("⊩", AMSSYMB), r"\vDash": ("⊨", AMSSYMB), r"\nmid": ("∤", AMSSYMB),
    r"\nvDash": ("⊭", AMSSYMB), r"\nsubseteq": ("⊈", AMSSYMB),
    r"\subsetneq": ("⊊", AMSSYMB), r"\varsubsetneq": ("⊊", AMSSYMB),
    r"\geqslant": ("⩾", AMSSYMB), r"\leqslant": ("⩽", AMSSYMB),
    r"\gtrless": ("≷", AMSSYMB), r"\lesssim": ("≲", AMSSYMB),
    r"\gtrsim": ("≳", AMSSYMB), r"\trianglelefteq": ("⊴", AMSSYMB),
    r"\blacktriangleright": ("▶", AMSSYMB), r"\triangleq": ("≜", AMSSYMB),
    r"\backsim": ("∽", AMSSYMB), r"\leadsto": ("⇝", AMSSYMB),
    r"\circlearrowleft": ("↺", AMSSYMB), r"\circlearrowright": ("↻", AMSSYMB),
    r"\rightleftarrows": ("⇄", AMSSYMB), r"\rightrightarrows": ("⇉", AMSSYMB),
    r"\rightsquigarrow": ("⇝", AMSSYMB), r"\curvearrowright": ("↷", AMSSYMB),
    r"\twoheadrightarrow": ("↠", AMSSYMB), r"\nRightarrow": ("⇏", AMSSYMB),
    r"\nrightarrow": ("↛", AMSSYMB), r"\upharpoonright": ("↾", AMSSYMB),
    r"\nexists": ("∄", AMSSYMB), r"\sphericalangle": ("∢", AMSSYMB),
    r"\square": ("□", AMSSYMB), r"\blacksquare": ("■", AMSSYMB),
    r"\lozenge": ("◊", AMSSYMB), r"\varnothing": ("∅", AMSSYMB),
    r"\vartriangle": ("▵", AMSSYMB), r"\triangledown": ("▿", AMSSYMB),
    r"\mathbb{R}": ("ℝ", AMSSYMB), r"\mathbb{Q}": ("ℚ", AMSSYMB),
    r"\mathbb{N}": ("ℕ", AMSSYMB), r"\mathbb{Z}": ("ℤ", AMSSYMB),
    r"\mathbb{H}": ("ℍ", AMSSYMB), r"\mathfrak{A}": ("𝔄", AMSSYMB),
    r"\mathfrak{M}": ("𝔐", AMSSYMB), r"\mathfrak{S}": ("𝔖", AMSSYMB),
    r"\mathfrak{X}": ("𝔛", AMSSYMB),
    # other packages
    r"\mathbb{1}": ("𝟙", "bbold"),
    r"\mathds{1}": ("𝟙", "dsfont"), r"\mathds{C}": ("ℂ", "dsfont"),
    r"\mathds{E}": ("𝔼", "dsfont"), r"\mathds{N}": ("ℕ", "dsfont"),
    r"\mathds{P}": ("ℙ", "dsfont"), r"\mathds{Q}": ("ℚ", "dsfont"),
    r"\mathds{R}": ("ℝ", "dsfont"), r"\mathds{Z}": ("ℤ", "dsfont"),
    r"\mathscr{A}": ("𝒜", "mathrsfs"), r"\mathscr{C}": ("𝒞", "mathrsfs"),
    r"\mathscr{D}": ("𝒟", "mathrsfs"), r"\mathscr{E}": ("ℰ", "mathrsfs"),
    r"\mathscr{F}": ("ℱ", "mathrsfs"), r"\mathscr{H}": ("ℋ", "mathrsfs"),
    r"\mathscr{L}": ("ℒ", "mathrsfs"), r"\mathscr{P}": ("𝒫", "mathrsfs"),
    r"\mathscr{S}": ("𝒮", "mathrsfs"),
    r"\fint": ("⨏", "esint"), r"\oiint": ("∯", "esint"), r"\varoiint": ("∯", "esint"),
    r"\llbracket": ("⟦", "stmaryrd"), r"\rrbracket": ("⟧", "stmaryrd"),
    r"\mapsfrom": ("↤", "stmaryrd"), r"\shortrightarrow": ("→", "stmaryrd"),
    r"\parr": ("⅋", "cmll"), r"\with": ("&", "cmll"),
    r"\iddots": ("⋰", "mathdots"), r"\dotsc": ("…", "amsmath"),
    r"\celsius": ("℃", "gensymb"), r"\degree": ("°", "gensymb"), r"\ohm": ("Ω", "gensymb"),
    r"\venus": ("♀", "wasysym"), r"\mars": ("♂", "wasysym"),
    r"\female": ("♀", "wasysym"), r"\male": ("♂", "wasysym"),
    r"\astrosun": ("☉", "wasysym"), r"\sun": ("☼", "wasysym"),
    r"\fullmoon": ("○", "wasysym"), r"\leftmoon": ("☾", "wasysym"),
    r"\checked": ("✓", "wasysym"), r"\diameter": ("⌀", "wasysym"),
    r"\lightning": ("↯", "wasysym"), r"\Bowtie": ("⋈", "stix"),
    r"\mathsection": ("§", None),
}


def describe(latex):
    """Return {"latex", "unicode", "package"?} for a symbol's LaTeX code."""
    if latex in _PACKAGED:
        uni, pkg = _PACKAGED[latex]
    elif latex in _GREEK:
        uni, pkg = _GREEK[latex], None
    elif latex in _SYMBOLS:
        uni, pkg = _SYMBOLS[latex], None
    elif len(latex) == 1:
        uni, pkg = latex, None
    else:
        uni, pkg = None, None
    out = {"latex": latex, "unicode": uni}
    if pkg:
        out["package"] = pkg
    return out
