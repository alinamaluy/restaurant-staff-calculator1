import streamlit as st
import pandas as pd
from math import ceil
from datetime import datetime

# 🎯 Функция расчета
def calculate_staff_from_orders(
    orders_per_day,
    order_norm_per_waiter,
    shifts_per_day,
    restaurant_days_per_week,
    waiter_days_per_week,
    shifts_per_waiter_per_day,
    position="Официант"
):
    total_orders_per_week = orders_per_day * restaurant_days_per_week
    orders_per_shift = orders_per_day / shifts_per_day
    waiters_per_shift = ceil(orders_per_shift / order_norm_per_waiter)
    total_weekly_shifts = waiters_per_shift * shifts_per_day * restaurant_days_per_week
    effective_shifts_per_waiter = waiter_days_per_week * shifts_per_waiter_per_day
    required_waiters = ceil(total_weekly_shifts / effective_shifts_per_waiter)

    data = {
        "Должность": position,
        "Заказов в день": f"{orders_per_day}",
        "Смен в день": f"{shifts_per_day}",
        "Норма заказов на 1 официанта": f"{order_norm_per_waiter}",
        "Заказов в смену": f"{orders_per_shift:.1f}",
        "Официантов на смену": f"{waiters_per_shift}",
        "Смен в неделю (всего)": f"{total_weekly_shifts}",
        "Смен в неделю (1 сотрудник)": f"{effective_shifts_per_waiter}",
        "Необходимое количество сотрудников": f"{required_waiters}"
    }

    return pd.DataFrame.from_dict(data, orient='index', columns=["Значение"])

# 🌐 Интерфейс Streamlit
st.set_page_config(page_title="Расчет штата по заказам", layout="centered")
st.title("📊 Расчет количества сотрудников ресторана")
st.markdown("Введите параметры ниже для расчета нужного количества официантов:")

with st.form("input_form"):
    position = st.text_input("Должность", value="Официант")
    orders_per_day = st.slider("Заказов в день", 20, 500, 120, step=10)
    order_norm = st.slider("Норма заказов на 1 официанта", 10, 100, 30, step=5)
    shifts_per_day = st.slider("Смен в день", 1, 3, 2)
    restaurant_days = st.slider("Дней работы ресторана в неделю", 1, 7, 7)
    waiter_days = st.slider("Дней работы 1 официанта в неделю", 1, 7, 5)
    shifts_per_waiter = st.slider("Смен в день на 1 официанта", 1, 2, 1)

    submitted = st.form_submit_button("🔍 Рассчитать")

if submitted:
    df = calculate_staff_from_orders(
        orders_per_day,
        order_norm,
        shifts_per_day,
        restaurant_days,
        waiter_days,
        shifts_per_waiter,
        position
    )

    st.success("✅ Расчет завершен!")
    st.dataframe(df)

    # 💾 Скачивание Excel
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"staff_calculation_{now}.xlsx"
    df.to_excel(filename)

    with open(filename, "rb") as f:
        st.download_button("📥 Скачать результат в Excel", f, file_name=filename)
