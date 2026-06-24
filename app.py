import streamlit as st
import time

# --- DATA (From BIO 102 Lecture Notes) ---

# --- APP UI ---
st.set_page_config(page_title="BIO 102 Exam")
st.title("🎓 BIO 102 Pro Exam")
# --- DATA (From BIO 102 Lecture Notes) ---
questions = [
    {"q": "What is an ecological adaptation?", "a": "Traits enabling survival and reproduction", "opts": ["Genetic mutation", "Traits enabling survival and reproduction", "Only physical changes"], "exp": "Adaptations are morphological, physiological, or behavioral attributes enabling survival and reproduction."},
    {"q": "Plants adapted to high light intensity are?", "a": "Heliophytes", "opts": ["Sciophytes", "Heliophytes", "Hydrophytes"], "exp": "Heliophytes are plants adapted to high light intensity."},
    {"q": "Which of these is a free-floating hydrophyte?", "a": "Eichhornia", "opts": ["Eichhornia", "Hydrilla", "Sagittaria"], "exp": "Eichhornia floats freely on the water."},
    {"q": "Rooted submerged hydrophytes do not interact with?", "a": "Air", "opts": ["Soil", "Water", "Air"], "exp": "Rooted submerged hydrophytes are completely immersed and do not interact with air."},
    {"q": "Plants that complete their life cycle in 4-6 weeks are?", "a": "Ephemeral", "opts": ["Succulents", "Ephemeral", "Non-succulents"], "exp": "Ephemeral plants complete their life cycle in a short period during rains."},
    {"q": "Which plant stores water in its leaves?", "a": "Aloe", "opts": ["Opuntia", "Aloe", "Asparagus"], "exp": "Succulents are stored in leaves (Aloe, Agave)."},
    {"q": "Plants growing in saline habitats are called?", "a": "Halophytes", "opts": ["Mesophytes", "Xerophytes", "Halophytes"], "exp": "Plants adapted to growing in saline habitats are called halophytes."},
    {"q": "What is the primary mode of nutrition in plants?", "a": "Photoautotrophy", "opts": ["Heterotrophy", "Photoautotrophy", "Mixotrophy"], "exp": "Plants primarily rely on photoautotrophy."},
    {"q": "Which parasite uses haustoria to extract nutrients?", "a": "Rafflesia", "opts": ["Rafflesia", "Indian Pipe", "Venus Flytrap"], "exp": "Parasitic plants extract nutrients using specialized roots called haustoria."},
    {"q": "What is Batesian mimicry?", "a": "Edible animal mimics a harmful one", "opts": ["Two unpalatable species mimic", "Edible animal mimics a harmful one", "Predator mimics prey"], "exp": "Batesian mimicry is when an unprotected and edible animal mimics another that is protected and unpalatable."},
    {"q": "What is Mullerian mimicry?", "a": "Two unpalatable species mimic each other", "opts": ["Predator mimics prey", "Two unpalatable species mimic each other", "Dead plant mimicry"], "exp": "Mullerian mimicry is when two or more unpalatable species mimic each other."},
    {"q": "How do bats navigate?", "a": "Echolocation", "opts": ["Camouflage", "Mimicry", "Echolocation"], "exp": "Bats produce high-frequency sound which produces echoes on the principle of sonar."},
    {"q": "Which animal plays dead when sensing danger?", "a": "American opossum", "opts": ["Kangaroo rat", "American opossum", "Camel"], "exp": "American opossum (Didelphis) stays like a dead animal when it senses any danger."},
    {"q": "Metabolic water provides what percentage of a desert rat's needs?", "a": "90%", "opts": ["50%", "75%", "90%"], "exp": "90% of a desert rat's water requirement is met from metabolic water."},
    {"q": "How do plants prevent herbivory?", "a": "Thorns, spines, and chemicals", "opts": ["Faster growth", "Thorns, spines, and chemicals", "Changing color"], "exp": "To prevent herbivory, plants developed thorns, spines, and chemicals."},
    {"q": "What are animals that feed on decomposing matter?", "a": "Detritivores", "opts": ["Herbivores", "Carnivores", "Detritivores"], "exp": "Detritivores feed on dead, decomposing organic matter."},
    {"q": "Giant tube worms at hydrothermal vents rely on?", "a": "Chemoautotrophic bacteria", "opts": ["Photosynthesis", "Chemoautotrophic bacteria", "Ingesting particles"], "exp": "Giant tube worms rely on symbiotic bacteria that use hydrogen sulfide to produce organic molecules."},
    {"q": "Animals that can withstand sub-zero temperatures are?", "a": "Freeze-tolerant", "opts": ["Freeze-tolerant", "Migratory", "Aestivating"], "exp": "Freeze-tolerant animals possess ice-nucleating proteins that induce ice formation in extracellular spaces."},
    {"q": "What does a Camel do during non-availability of water?", "a": "Stores urea", "opts": ["Sweats", "Stores urea", "Produces urine"], "exp": "During periods of non-availability of water, the animal stores urea and does not produce urine."},
    {"q": "What are the three main types of ecological adaptation?", "a": "Structural, behavioral, physiological", "opts": ["Structural, behavioral, physiological", "Light, water, salt", "Feeding, migration, mimicry"], "exp": "There are three main types: structural, behavioral, and physiological adaptation."}
]

if 'score' not in st.session_state: st.session_state.score = 0
if 'q_index' not in st.session_state: st.session_state.q_index = 0
if 'submitted' not in st.session_state: st.session_state.submitted = False

name = st.text_input("Enter your name to begin:")

if st.button("Start Exam"):
    if name:
        st.session_state.start_time = time.time()
        st.session_state.submitted = False
    else:
        st.error("Please enter your name.")

if 'start_time' in st.session_state and not st.session_state.submitted:
    elapsed = time.time() - st.session_state.start_time
    remaining = 300 - elapsed
    
    if remaining > 0:
        st.metric("Time Remaining", f"{int(remaining // 60)}:{int(remaining % 60):02d}")
        q = questions[st.session_state.q_index]
        st.subheader(f"Q{st.session_state.q_index + 1}: {q['q']}")
        ans = st.radio("Options:", q['opts'], key=f"q{st.session_state.q_index}")
        
        if st.button("Next Question"):
            if ans == q['a']: st.session_state.score += 1
            if st.session_state.q_index < len(questions) - 1:
                st.session_state.q_index += 1
                st.rerun()
            else:
                st.session_state.submitted = True
                st.rerun()
    else:
        st.error("Time's up!")
        st.session_state.submitted = True

if st.session_state.submitted:
    st.write(f"Exam Finished, {name}!")
    percent = (st.session_state.score / len(questions)) * 100
    st.write(f"Your Score: {st.session_state.score}/{len(questions)} ({percent:.1f}%)")
    st.subheader("Answer Key & Review:")
    for q in questions:
        with st.expander(q['q']):
            st.write(f"**Correct Answer:** {q['a']}")
            st.write(f"**Explanation:** {q['exp']}")
