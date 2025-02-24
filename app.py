import streamlit as st
import numpy as np
import time

def bellman_equation(n, k):
    n, k = max(1, n), max(1, k)
    dp = [[0 for _ in range(k + 1)] for _ in range(n + 1)]
    for i in range(1, n + 1):
        dp[i][0], dp[i][1] = 0, 1
    for j in range(1, k + 1):
        dp[1][j] = j
    for i in range(2, n + 1):
        for j in range(2, k + 1):
            dp[i][j] = min(1 + max(dp[i-1][x-1], dp[i][j-x]) for x in range(1, j+1))
    return dp[n][k]

def optimal_floor(n, k, prev_floor):
    if n <= 1 or k <= 1:
        return prev_floor + 1
    min_drops = bellman_equation(n, k)
    for x in range(1, k + 1):
        if 1 + max(x - 1, bellman_equation(n - 1, k - x)) == min_drops:
            return prev_floor + x
    return prev_floor + 1

def animate_egg_drop(start_floor, end_floor, breaks):
    placeholder = st.empty()
    for floor in range(start_floor, end_floor + 1):
        placeholder.markdown(f"""
        👻 Boo! I'm watching you!
        
        🏢 Floor {floor}
        
        🥚
        """)
        time.sleep(0.1)
    if breaks:
        placeholder.markdown("""
        👻 Oops! I told you so!
        
        🏢
        
        💥 Egg broke!
        """)
    else:
        placeholder.markdown("""
        👻 Lucky you!
        
        🏢
        
        ✅ Egg survived!
        """)
    time.sleep(1)
    placeholder.empty()

def main():
    st.set_page_config(page_title="Egg Drop Challenge", page_icon="🥚")
    st.title("🏢 Egg Drop Challenge 🥚")
    st.write("Find the highest floor where the egg survives the drop!")

    col1, col2 = st.columns(2)
    with col1:
        total_floors = st.number_input("Number of Floors", min_value=1, max_value=1000, value=100)
    with col2:
        total_eggs = st.number_input("Number of Eggs", min_value=1, max_value=10, value=2)

    if 'game_state' not in st.session_state or st.session_state.game_state['total_floors'] != total_floors or st.session_state.game_state['total_eggs'] != total_eggs:
        optimal_solution = bellman_equation(total_eggs, total_floors)
        st.session_state.game_state = {
            'critical_floor': np.random.randint(1, total_floors + 1),
            'total_floors': total_floors,
            'total_eggs': total_eggs,
            'eggs_left': total_eggs,
            'drops': 0,
            'game_over': False,
            'ghost_hint': "",
            'last_safe_floor': 0,
            'optimal_solution': optimal_solution
        }

    st.sidebar.markdown("### 📊 Game Status")
    st.sidebar.markdown(f"🏢 Total Floors: {total_floors}")
    st.sidebar.markdown(f"🥚 Eggs Left: {st.session_state.game_state['eggs_left']}")
    st.sidebar.markdown(f"🎯 Drops Made: {st.session_state.game_state['drops']}")
    st.sidebar.markdown(f"🎓 Optimal Solution: {st.session_state.game_state['optimal_solution']} drops")

    if st.session_state.game_state['ghost_hint']:
        st.info(f"👻 Ghost's Hint: {st.session_state.game_state['ghost_hint']}")

    floor = st.slider("Choose a floor to drop the egg", 
                      st.session_state.game_state['last_safe_floor'] + 1, 
                      total_floors, 
                      optimal_floor(st.session_state.game_state['eggs_left'], 
                                    total_floors - st.session_state.game_state['last_safe_floor'], 
                                    st.session_state.game_state['last_safe_floor']))
    
    if st.button("Drop Egg 🥚"):
        if not st.session_state.game_state['game_over']:
            st.session_state.game_state['drops'] += 1
            
            animate_egg_drop(st.session_state.game_state['last_safe_floor'] + 1, floor, floor >= st.session_state.game_state['critical_floor'])
            
            if floor >= st.session_state.game_state['critical_floor']:
                st.session_state.game_state['eggs_left'] -= 1
                st.error(f"💥 Egg broke at floor {floor}!")
                if st.session_state.game_state['eggs_left'] == 0:
                    st.session_state.game_state['game_over'] = True
                    st.warning(f"Game Over! You've used all your eggs. The critical floor was {st.session_state.game_state['critical_floor']}.")
                    st.session_state.game_state['ghost_hint'] = f"Ha! Couldn't figure it out, huh? It was floor {st.session_state.game_state['critical_floor']} all along! 👻"
                else:
                    st.session_state.game_state['ghost_hint'] = "Seriously? You should've gone lower! 😒"
            else:
                st.success(f"✅ Egg survived the drop from floor {floor}!")
                st.session_state.game_state['last_safe_floor'] = floor
                if floor < st.session_state.game_state['critical_floor'] - 10:
                    st.session_state.game_state['ghost_hint'] = "Come on! Go higher, genius! 🤓"
                elif floor < st.session_state.game_state['critical_floor']:
                    st.session_state.game_state['ghost_hint'] = "Getting warmer! Try a bit higher, okay? 😏"
                else:
                    st.session_state.game_state['ghost_hint'] = "You're really close! Just a bit more... 🤔"
            
            if floor == st.session_state.game_state['critical_floor'] or st.session_state.game_state['drops'] == st.session_state.game_state['optimal_solution']:
                st.session_state.game_state['game_over'] = True
                st.balloons()
                st.success(f"🎉 Congratulations! You found the critical floor ({st.session_state.game_state['critical_floor']}) in {st.session_state.game_state['drops']} drops!")
                st.session_state.game_state['ghost_hint'] = "Finally! You listened! 👻"

    st.progress(st.session_state.game_state['eggs_left'] / st.session_state.game_state['total_eggs'])

    if st.button("New Game 🔄"):
        optimal_solution = bellman_equation(total_eggs, total_floors)
        st.session_state.game_state = {
            'critical_floor': np.random.randint(1, total_floors + 1),
            'total_floors': total_floors,
            'total_eggs': total_eggs,
            'eggs_left': total_eggs,
            'drops': 0,
            'game_over': False,
            'ghost_hint': "",
            'last_safe_floor': 0,
            'optimal_solution': optimal_solution
        }
        st.experimental_rerun()

    with st.expander("How to Play"):
        st.write("""
        1. Choose the number of floors and eggs.
        2. Select a floor to drop the egg from.
        3. Click 'Drop Egg' to see if it breaks.
        4. Use the ghost's hints and optimal strategy to find the highest safe floor.
        5. Game ends when you find the critical floor, reach the optimal solution, or run out of eggs.
        6. Try to find the critical floor in the fewest drops!
        """)

if __name__ == "__main__":
    main()


