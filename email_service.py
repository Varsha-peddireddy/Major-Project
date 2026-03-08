import yagmail
import mysql.connector

# -------- DATABASE CONNECTION --------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Varsha@14",
    database="traffic_db"
)

cursor = db.cursor()

# -------- EMAIL CONFIG --------
sender_email = "working122614@gmail.com"
app_password = "hsvjdfgnlzaqgqub"


def send_challan(vehicle_number, fine_amount):
    try:
        print("\n==============================")
        print("Vehicle received from GUI:", vehicle_number)

        vehicle_number = vehicle_number.strip()

        query = """
        SELECT email 
        FROM vehicle_owners 
        WHERE LOWER(vehicle_number) = LOWER(%s)
        """

        cursor.execute(query, (vehicle_number,))
        result = cursor.fetchone()

        print("Database result:", result)

        if result:
            receiver_email = result[0]
            print("Sending email to:", receiver_email)

            subject = "Traffic E-Challan Notice"

            body = f"""
Dear Citizen,

Your vehicle {vehicle_number} violated traffic rules.
Fine Amount: ₹{fine_amount}

Please pay within 7 days.

Traffic Department
"""

            # Create yag inside function
            yag = yagmail.SMTP(sender_email, app_password)

            yag.send(
                to=receiver_email,
                subject=subject,
                contents=body
            )

            yag.close()

            print("✅ Email SENT successfully!")
            print("==============================\n")

        else:
            print("❌ Vehicle number NOT FOUND in database!")
            print("==============================\n")

    except Exception as e:
        print("❌ ERROR while sending email:", str(e))
        print("==============================\n")