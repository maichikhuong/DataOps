import streamlit as st

# 👇 Tất cả code liên quan giao diện đặt trong hàm main()
def main():
    st.title("Demo App")
    st.write("Chào bạn! Đây là giao diện chạy bằng Streamlit.")
    
    # Thêm một input box và hiển thị kết quả
    name = st.text_input("Nhập tên của bạn:")
    if name:
        st.success(f"Xin chào {name} 👋")

    # Thêm một slider
    number = st.slider("Chọn một số", 0, 100, 50)
    st.write("Bạn vừa chọn:", number)

# 👇 Chỉ gọi main() khi chạy bằng streamlit run
if __name__ == "__main__":
    main()