import random
import string
import streamlit as st

st.set_page_config(page_title="Password Generator", page_icon="🔐")
st.title("🔐 Password Generator")


def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    charset = ""
    if use_upper:   charset += string.ascii_uppercase
    if use_lower:   charset += string.ascii_lowercase
    if use_digits:  charset += string.digits
    if use_symbols: charset += string.punctuation

    if not charset:
        return None

    guaranteed = []
    if use_upper:   guaranteed.append(random.choice(string.ascii_uppercase))
    if use_lower:   guaranteed.append(random.choice(string.ascii_lowercase))
    if use_digits:  guaranteed.append(random.choice(string.digits))
    if use_symbols: guaranteed.append(random.choice(string.punctuation))

    remaining = [random.choice(charset) for _ in range(length - len(guaranteed))]
    password_list = guaranteed + remaining
    random.shuffle(password_list)
    return "".join(password_list)


def get_strength(length, use_upper, use_lower, use_digits, use_symbols):
    variety = sum([use_upper, use_lower, use_digits, use_symbols])
    if length >= 16 and variety >= 3:
        return "Strong 💪", "green"
    elif length >= 10 and variety >= 2:
        return "Medium ⚠️", "orange"
    else:
        return "Weak ❌", "red"


# ── Controls ─────────────────────────────────────────────────────────────────
length     = st.slider("Password Length", 4, 64, 12)
use_upper  = st.checkbox("Uppercase (A–Z)",    value=True)
use_lower  = st.checkbox("Lowercase (a–z)",    value=True)
use_digits = st.checkbox("Numbers (0–9)",      value=True)
use_syms   = st.checkbox("Symbols (!@#$...)",  value=False)
count      = st.number_input("How many passwords", min_value=1, max_value=10, value=1)

if st.button("Generate Password", type="primary"):
    if not any([use_upper, use_lower, use_digits, use_syms]):
        st.warning("Select at least one character type.")
    else:
        passwords = [generate_password(length, use_upper, use_lower, use_digits, use_syms)
                     for _ in range(count)]
        st.code("\n".join(passwords), language=None)

        label, color = get_strength(length, use_upper, use_lower, use_digits, use_syms)
        st.markdown(f"**Strength:** :{color}[{label}]")
