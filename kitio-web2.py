# Ψηφιακό Κυτίο Έκφρασης Γνώμης Μαθητή/τριας

import streamlit as st

# Ρύθμιση σελίδας
st.set_page_config(page_title="Ψηφιακό Κουτί Έκφρασης", page_icon="💡", layout="centered")

# Αρχικοποίηση δεδομένων στη μνήμη της συνεδρίας
if 'entries' not in st.session_state:
    st.session_state.entries = []
if 'counter' not in st.session_state:
    st.session_state.counter = 1

st.title("💡 Ψηφιακό Κυτίο Έκφρασης Γνώμης")
st.write("Εκφράστε τις ιδέες, τα αιτήματα ή τα θετικά σας σχόλια για τη σχολική μας κοινότητα.")

# Πλευρικό μενού πλοήγησης
menu = st.sidebar.selectbox("Επιλογή Ενέργειας", ["Υποβολή Νέας Σκέψης", "Προβολή Καταγραφών", "Στατιστικά"])

# --- 1. ΥΠΟΒΟΛΗ ---
if menu == "Υποβολή Νέας Σκέψης":
    st.subheader("📝 Υποβολή νέου μηνύματος")
    
    with st.form("entry_form"):
        author = st.text_input("Όνομα αποστολέα (αφήστε κενό για ανώνυμος/η):")
        category = st.selectbox(
            "Κατηγορία:",
            ["💡 Ιδέες & Προτάσεις", "🔧 Ζητήματα & Δυσκολίες", "❤️ Θετικά Σχόλια & Ευχαριστώ"]
        )
        description = st.text_area("Γράψτε το μήνυμά σας:")
        
        submitted = st.form_submit_button("Υποβολή Μηνύματος")
        
        if submitted:
            if not author.strip():
                author = "Ανώνυμος/η"
            if description.strip():
                new_entry = {
                    "id": st.session_state.counter,
                    "author": author,
                    "category": category,
                    "description": description,
                    "status": "Εκκρεμεί"
                }
                st.session_state.entries.append(new_entry)
                st.success(f"Επιτυχής καταγραφή! Δόθηκε κωδικός αναφοράς: #{st.session_state.counter}")
                st.session_state.counter += 1
            else:
                st.warning("Παρακαλώ συμπληρώστε την περιγραφή του μηνύματος.")

# --- 2. ΠΡΟΒΟΛΗ & ΔΙΑΧΕΙΡΙΣΗ ---
elif menu == "Προβολή Καταγραφών":
    st.subheader("📋 Λίστα Καταγραφών Τάξης")
    
    if not st.session_state.entries:
        st.info("Το κυτίο είναι προς το παρόν άδειο.")
    else:
        filter_cat = st.selectbox(
            "Φίλτρο ανά κατηγορία:", 
            ["Όλες", "💡 Ιδέες & Προτάσεις", "🔧 Ζητήματα & Δυσκολίες", "❤️ Θετικά Σχόλια & Ευχαριστώ"]
        )
        
        for e in st.session_state.entries:
            if filter_cat == "Όλες" or e["category"] == filter_cat:
                with st.expander(f"#{e['id']} | {e['category']} — [{e['status']}]"):
                    st.write(f"**Αποστολέας:** {e['author']}")
                    st.write(f"**Μήνυμα:** {e['description']}")
                    
                    # Δυνατότητα αλλαγής κατάστασης
                    status_list = ["Εκκρεμεί", "Υπό εξέταση", "Ολοκληρώθηκε"]
                    current_idx = status_list.index(e["status"])
                    new_status = st.selectbox(
                        "Αλλαγή κατάστασης:", 
                        status_list, 
                        index=current_idx, 
                        key=f"status_{e['id']}"
                    )
                    if new_status != e["status"]:
                        e["status"] = new_status
                        st.success(f"Η κατάσταση ενημερώθηκε σε: {new_status}")

# --- 3. ΣΤΑΤΙΣΤΙΚΑ ---
elif menu == "Στατιστικά":
    st.subheader("📊 Στατιστικά στοιχεία κυτίου")
    total = len(st.session_state.entries)
    
    st.metric(label="Συνολικές Καταγραφές", value=total)
    
    if total > 0:
        st.write("---")
        for cat in ["💡 Ιδέες & Προτάσεις", "🔧 Ζητήματα & Δυσκολίες", "❤️ Θετικά Σχόλια & Ευχαριστώ"]:
            count = sum(1 for e in st.session_state.entries if e["category"] == cat)
            st.write(f"- **{cat}**: {count} καταγραφές")