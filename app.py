import streamlit as st

# १. पेज कॉन्फिगरेशन
st.set_page_config(
    page_title="Balaji Cyber Point", page_icon="📱", layout="centered"
)

# २. पासवर्ड सेट करा
ADMIN_PASSWORD = "1234"  # तुमच्या आवडीनुसार हा पासवर्ड बदलू शकता

# ३. मुख्य नेव्हिगेशन (बाहेर फक्त २ टॅब दिसतील)
tab_home, tab_admin = st.tabs(["🏠 Home", "🔒 Admin Desk"])

# ==========================================
# 🏠 HOME TAB - केवळ मार्केटिंग आणि माहिती
# ==========================================
with tab_home:
    st.title("बालाजी सायबर पॉईंट (माणगाव)")
    st.subheader("तुमचे डिजिटल आणि ट्रॅव्हल सोल्यूशन पार्टनर!")

    st.image(
        "https://images.unsplash.com/photo-1542744094-3a31f103e35f?q=80&w=600",
        caption="Balaji Cyber Point",
    )

    st.write("---")
    st.markdown("### 🌟 आमच्या प्रमुख सेवा:")

    st.markdown("- **सर्व ऑनलाईन फॉर्म्स:** नोकरभरती, ॲडमिट कार्ड आणि हॉल तिकीट.")
    st.markdown(
        "- **शासकीय योजना:** घरकुल योजना, शबरी आवास योजना आणि इतर सरकारी अर्ज."
    )
    st.markdown(
        "- **ट्रॅव्हल बुकिंग:** देश-विदेशातील फ्लाईट्स, हॉटेल्स आणि टूर पॅकेजेस (MakeMyTrip)."
    )
    st.markdown(
        "- **कर आणि महसूल:** नगरपंचायत प्रॉपर्टी टॅक्स, वीज बिल आणि महाआयटी सेवा."
    )
    st.markdown(
        "- **डिजिटल फोटो टूल्स:** जुने फोटो 4K मध्ये रिस्टोर करणे आणि कॉम्प्युटर सायझिंग."
    )

    st.info("📍 पत्ता: बालाजी कॉम्प्लेक्स, माणगाव, रायगड, महाराष्ट्र")


# ==========================================
# 🔒 ADMIN DESK - लॉक केलेला विभाग
# ==========================================
with tab_admin:
    st.header("🔒 Admin Desk (Secure Area)")

    # सेशन स्टेटमध्ये लॉगिन स्टेटस ट्रॅक करणे
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    # जर लॉग इन नसेल तर पासवर्ड विचारा
    if not st.session_state.admin_logged_in:
        password_input = st.text_input(
            "कृपया ॲडमिन पासवर्ड टाका:", type="password"
        )
        login_btn = st.button("लॉगिन करा")

        if login_btn:
            if password_input == ADMIN_PASSWORD:
                st.session_state.admin_logged_in = True
                st.success("लॉगिन यशस्वी!")
                st.rerun()  # पेज रिफ्रेश करून टूल्स दाखवण्यासाठी
            else:
                st.error("चुकीचा पासवर्ड! कृपया पुन्हा प्रयत्न करा.")

    # जर लॉगिन यशस्वी झाले असेल तर आतील सर्व टूल्स दाखवा
    else:
        # लॉगआउट बटन
        if st.button("🔒 लॉक करा (Logout)"):
            st.session_state.admin_logged_in = False
            st.rerun()

        st.write("---")
        st.markdown("### ⚙️ तुमचे अंतर्गत टूल्स (Internal Tools)")

        # ॲडमिन डेस्कच्या आतील ३ मुख्य टॅब
        tool_bill, tool_data, tool_image = st.tabs(
            ["📊 Bill Manager", "📁 Cyber Data", "🖼️ Image Tool"]
        )

        # --- टॅब १: Bill Manager ---
        with tool_bill:
            st.subheader("📊 Bill Manager")
            st.info("येथे तुमचे बिलिंग आणि ट्रान्झॅक्शनचे व्यवस्थापन चालेल.")
            # तुमचा बिलिंगचा कोड किंवा इनपुट फॉर्म येथे येईल

        # --- टॅब २: Cyber Data ---
        with tool_data:
            st.subheader("📁 Cyber Data")
            st.info("येथे ग्राहकांचा डेटा, स्कॅन डॉक्युमेंट्स आणि रेकॉर्ड्स राहतील.")
            # तुमचा डेटाबेस किंवा फाईल अपलोडचा कोड येथे येईल

        # --- टॅब ३: Image Tool ---
        with tool_image:
            st.subheader("🖼️ Image Tool")
            st.info(
                "येथे तुम्ही फोटो आणि स्वाक्षरी (Signature) रिसाइझ करू शकता."
            )
            # तुमचा जुना इमेज रिसाइझरचा (width 160 x height 200) कोड थेट येथे जोडता येईल!
