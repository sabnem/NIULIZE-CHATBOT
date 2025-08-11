from django.core.management.base import BaseCommand
from chatbot.models import FAQ, FAQCategory

class Command(BaseCommand):
    help = 'Populates the database with AMCET college-specific FAQ entries'

    def handle(self, *args, **kwargs):
        # Create FAQ categories
        general_cat, _ = FAQCategory.objects.get_or_create(
            name="General Information",
            defaults={'description': 'Basic information about AMCET'}
        )
        
        admissions_cat, _ = FAQCategory.objects.get_or_create(
            name="Admissions",
            defaults={'description': 'Information about admission process and requirements'}
        )
        
        programs_cat, _ = FAQCategory.objects.get_or_create(
            name="Academic Programs",
            defaults={'description': 'Details about courses and programs offered'}
        )
        
        facilities_cat, _ = FAQCategory.objects.get_or_create(
            name="Facilities",
            defaults={'description': 'Information about campus facilities and resources'}
        )
        
        student_life_cat, _ = FAQCategory.objects.get_or_create(
            name="Student Life",
            defaults={'description': 'Information about student activities and campus life'}
        )

        fees_cat, _ = FAQCategory.objects.get_or_create(
            name="Fees and Funding",
            defaults={'description': 'Information about tuition fees and financial aid'}
        )

        # Sample FAQ entries
        faqs_data = [
            # General Information
            {
                'category': general_cat,
                'title': "What is AMCET?",
                'response': """Al-Makhtoum College of Engineering and Technology (AMCET) is a prestigious engineering institution dedicated to excellence in technical education. Established with a vision to create world-class engineers, AMCET offers state-of-the-art facilities and industry-aligned curriculum.

Key Features:
• Industry-experienced faculty
• Modern infrastructure
• Strong industry connections
• Focus on practical learning
• Research opportunities""",
                'keywords': "what is amcet, about amcet, college information, overview, introduction",
                'priority': 100,
            },
            {
                'category': general_cat,
                'title': "Where is AMCET located?",
                'response': """AMCET is located in a prime location with excellent connectivity:

📍 Address: [Insert College Address]
🚌 Transportation: Regular bus services available
🚉 Nearest Railway Station: [Station Name] (X km)
✈️ Nearest Airport: [Airport Name] (Y km)

The campus is easily accessible by public transport and private vehicles.""",
                'keywords': "location, address, where is amcet, how to reach, directions, map",
                'priority': 95,
            },
            # Admissions
            {
                'category': admissions_cat,
                'title': "What are the admission requirements?",
                'response': """Admission Requirements for AMCET:

📚 Academic Requirements:
• Minimum 65% in 10+2 with PCM
• Valid entrance exam score (KCET/COMEDK)

📝 Required Documents:
• 10th and 12th mark sheets
• Transfer certificate
• Character certificate
• Entrance exam score card
• 4 passport size photos
• ID proof

⏰ Important Dates:
• Application Start: [Date]
• Application Deadline: [Date]
• Academic Year Start: [Date]""",
                'keywords': "admission requirements, how to apply, eligibility, documents needed, application process",
                'priority': 90,
            },
            # Academic Programs
            {
                'category': programs_cat,
                'title': "What courses does AMCET offer?",
                'response': """AMCET offers various undergraduate and postgraduate engineering programs:

🎓 B.Tech Programs (4 years):
• Computer Science Engineering
• Mechanical Engineering
• Electrical & Electronics Engineering
• Civil Engineering
• Electronics & Communication

👨‍🔬 M.Tech Programs (2 years):
• Computer Science & Engineering
• Digital Electronics
• Structural Engineering
• Power Systems

Each program is designed with industry inputs and includes practical training.""",
                'keywords': "courses, programs, branches, departments, btech, mtech, engineering courses",
                'priority': 85,
            },
            # Facilities
            {
                'category': facilities_cat,
                'title': "What facilities are available at AMCET?",
                'response': """AMCET provides world-class facilities:

🏫 Academic Facilities:
• Modern classrooms with projectors
• Well-equipped laboratories
• Computer centers with high-speed internet
• Central library with digital resources

🏢 Other Facilities:
• Wi-Fi enabled campus
• Separate hostels for boys and girls
• Sports complex with indoor/outdoor facilities
• Cafeteria and food court
• Medical center
• Transportation facility
• 24/7 security

🔬 Research Facilities:
• Research labs
• Innovation center
• Project development center""",
                'keywords': "facilities, amenities, infrastructure, labs, library, hostel, campus facilities",
                'priority': 80,
            },
            # Student Life
            {
                'category': student_life_cat,
                'title': "What is student life like at AMCET?",
                'response': """AMCET offers a vibrant student life:

🎮 Extra-Curricular Activities:
• Technical clubs
• Cultural clubs
• Sports teams
• Student council

🎯 Events:
• Annual tech fest
• Cultural festival
• Sports meets
• Industry workshops
• Guest lectures

👥 Student Support:
• Career guidance cell
• Placement assistance
• Counseling services
• Alumni network

We encourage students to participate in various activities for holistic development.""",
                'keywords': "student life, campus life, activities, clubs, events, extra curricular",
                'priority': 75,
            },
            # Fees and Funding
            {
                'category': fees_cat,
                'title': "What are the fees and scholarship options?",
                'response': """Fees and Financial Information:

💰 Tuition Fees (Per Year):
• B.Tech: [Amount]
• M.Tech: [Amount]

🏠 Hostel Fees:
• Room Rent: [Amount]/year
• Mess Fees: [Amount]/year

🎓 Scholarship Options:
• Merit scholarships
• Government scholarships
• Sports scholarships
• Financial aid for deserving students

💳 Payment Options:
• EMI available
• Education loan assistance
• Online payment facility""",
                'keywords': "fees, cost, tuition fees, scholarship, financial aid, education loan, payment",
                'priority': 85,
            },
            {
                'category': admissions_cat,
                'title': "How can I apply to AMCET?",
                'response': """Application Process for AMCET:

1️⃣ Online Application:
• Visit college website [website]
• Fill online application form
• Upload required documents
• Pay application fee

2️⃣ Entrance Exam:
• Appear for KCET/COMEDK
• Submit score card

3️⃣ Counseling Process:
• Merit list announcement
• Document verification
• Seat allocation
• Fee payment

📞 Help Desk:
• Phone: [Number]
• Email: [Email]
• WhatsApp: [Number]""",
                'keywords': "how to apply, application process, admission process, entrance exam, counseling",
                'priority': 88,
            },
        ]

        # Create or update FAQ entries
        for faq_data in faqs_data:
            FAQ.objects.update_or_create(
                title=faq_data['title'],
                defaults={
                    'category': faq_data['category'],
                    'response': faq_data['response'],
                    'keywords': faq_data['keywords'],
                    'priority': faq_data['priority'],
                    'is_active': True,
                }
            )

        self.stdout.write(self.style.SUCCESS('Successfully populated AMCET FAQ database!'))
