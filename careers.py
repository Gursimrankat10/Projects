import random


QUESTIONS = [
    {"id": "analysis_1", "dimension": "analytical", "prompt": "I like breaking a complicated problem into smaller parts before solving it."},
    {"id": "analysis_2", "dimension": "analytical", "prompt": "I enjoy comparing evidence and spotting patterns other people might miss."},
    {"id": "analysis_3", "dimension": "analytical", "prompt": "I can stay curious when the answer to a problem is not immediately clear."},
    {"id": "technology_1", "dimension": "technology", "prompt": "I enjoy learning how digital tools, machines, or systems work."},
    {"id": "technology_2", "dimension": "technology", "prompt": "I would like to build, configure, or improve a technical tool."},
    {"id": "technology_3", "dimension": "technology", "prompt": "I feel comfortable trying unfamiliar software or technology."},
    {"id": "creative_1", "dimension": "creative", "prompt": "I enjoy coming up with original ideas, designs, stories, or experiences."},
    {"id": "creative_2", "dimension": "creative", "prompt": "I like having room to experiment with different ways to solve a problem."},
    {"id": "creative_3", "dimension": "creative", "prompt": "I enjoy making something that communicates a clear idea or feeling."},
    {"id": "people_1", "dimension": "people", "prompt": "I feel motivated when I can help another person make progress."},
    {"id": "people_2", "dimension": "people", "prompt": "I am interested in understanding what other people need and experience."},
    {"id": "people_3", "dimension": "people", "prompt": "I enjoy working with people whose experiences differ from my own."},
    {"id": "detail_1", "dimension": "detail", "prompt": "I notice small errors and like checking work for accuracy."},
    {"id": "detail_2", "dimension": "detail", "prompt": "I enjoy organizing information so that it is easy to understand and use."},
    {"id": "detail_3", "dimension": "detail", "prompt": "I can follow careful procedures when precision matters."},
    {"id": "practical_1", "dimension": "practical", "prompt": "I like hands-on work that produces something I can see or test."},
    {"id": "practical_2", "dimension": "practical", "prompt": "I would enjoy troubleshooting equipment, materials, or real-world systems."},
    {"id": "practical_3", "dimension": "practical", "prompt": "I learn well by trying a task rather than only reading about it."},
    {"id": "leadership_1", "dimension": "leadership", "prompt": "I am comfortable helping a group agree on a plan and next steps."},
    {"id": "leadership_2", "dimension": "leadership", "prompt": "I enjoy taking responsibility for moving a shared project forward."},
    {"id": "leadership_3", "dimension": "leadership", "prompt": "I can make a considered decision even when there is no perfect option."},
    {"id": "science_1", "dimension": "science", "prompt": "I am curious about how nature, health, or the physical world works."},
    {"id": "science_2", "dimension": "science", "prompt": "I enjoy testing an explanation against evidence or observation."},
    {"id": "science_3", "dimension": "science", "prompt": "I would enjoy learning specialized scientific or technical knowledge."},
    {"id": "communication_1", "dimension": "communication", "prompt": "I enjoy explaining a complicated idea in a clear, useful way."},
    {"id": "communication_2", "dimension": "communication", "prompt": "I like writing, presenting, listening, or creating content for an audience."},
    {"id": "communication_3", "dimension": "communication", "prompt": "I adapt how I communicate depending on who I am speaking with."},
    {"id": "organization_1", "dimension": "organization", "prompt": "I enjoy planning work and keeping track of deadlines or moving parts."},
    {"id": "organization_2", "dimension": "organization", "prompt": "I feel satisfied when I make a confusing process work more smoothly."},
    {"id": "organization_3", "dimension": "organization", "prompt": "I can balance several responsibilities without losing sight of priorities."},
    {"id": "environment_1", "dimension": "environment", "prompt": "I care about protecting the natural environment and its resources."},
    {"id": "environment_2", "dimension": "environment", "prompt": "I am interested in how communities can become healthier and more sustainable."},
    {"id": "service_1", "dimension": "service", "prompt": "I find meaning in work that improves people's wellbeing or access to support."},
    {"id": "service_2", "dimension": "service", "prompt": "I can be patient and respectful when someone needs care or guidance."},
    {"id": "independence_1", "dimension": "independence", "prompt": "I enjoy having focus time to plan and complete work independently."},
    {"id": "independence_2", "dimension": "independence", "prompt": "I am comfortable setting my own learning goals and following through."},
    {"id": "entrepreneurship_1", "dimension": "entrepreneurship", "prompt": "I notice unmet needs and imagine useful products or services."},
    {"id": "entrepreneurship_2", "dimension": "entrepreneurship", "prompt": "I am willing to test an idea, learn from feedback, and revise it."},
]

CAREERS = [
    {
        "id": "software-developer",
        "title": "Software Developer",
        "category": "Technology & engineering",
        "icon": "</>",
        "description": "Build useful digital products by turning problems into clear, testable code.",
        "dimensions": {"analytical": 1.0, "technology": 1.0, "creative": 0.4, "people": 0.2, "detail": 0.7, "practical": 0.3, "leadership": 0.2},
        "strengths": ["Logical problem-solving", "Curiosity about technology", "Patience with iteration"],
        "first_step": "Build a small website or automate a task that interests you.",
        "project": "Build a tiny Python program or webpage that solves one problem you personally have.",
        "source_note": "Locally curated career overview; verify training and licensing requirements in your region.",
        "roadmap": [
            {"phase": "Explore", "duration": "Week 1", "items": ["Try a beginner coding lesson", "Notice which problems you enjoy solving", "Talk to a developer about their daily work"]},
            {"phase": "Build foundations", "duration": "Weeks 2–4", "items": ["Learn Python basics and core programming concepts", "Practice with small exercises", "Use Git to save and track your work"]},
            {"phase": "Make a project", "duration": "Weeks 5–8", "items": ["Choose a useful, manageable project", "Build it in small steps", "Write a short README and ask for feedback"]},
        ],
    },
    {
        "id": "data-analyst",
        "title": "Data Analyst",
        "category": "Data & research",
        "icon": "▤",
        "description": "Find patterns in data and explain what they mean so teams can make better decisions.",
        "dimensions": {"analytical": 1.0, "technology": 0.6, "creative": 0.3, "people": 0.5, "detail": 0.9, "practical": 0.3, "leadership": 0.3},
        "strengths": ["Analytical thinking", "Attention to detail", "Clear communication"],
        "first_step": "Explore a public dataset and write down three questions it could answer.",
        "project": "Analyze a small public dataset and present one chart with a careful, evidence-based explanation.",
        "source_note": "Locally curated career overview; verify training and licensing requirements in your region.",
        "roadmap": [
            {"phase": "Explore", "duration": "Week 1", "items": ["Look at examples of data storytelling", "Try a small public dataset", "Write questions that interest you"]},
            {"phase": "Build foundations", "duration": "Weeks 2–4", "items": ["Practice spreadsheets and basic statistics", "Learn SQL fundamentals", "Create clear charts from a dataset"]},
            {"phase": "Make a project", "duration": "Weeks 5–8", "items": ["Choose a dataset and investigate a question", "Summarize findings in a simple dashboard", "Share a short, evidence-based recommendation"]},
        ],
    },
    {
        "id": "ux-designer",
        "title": "UX Designer",
        "category": "Design & product",
        "icon": "✳",
        "description": "Make websites and apps easier to understand by combining design, research, and empathy.",
        "dimensions": {"analytical": 0.5, "technology": 0.4, "creative": 1.0, "people": 0.9, "detail": 0.6, "practical": 0.3, "leadership": 0.4},
        "strengths": ["Empathy and curiosity", "Visual problem-solving", "Learning from feedback"],
        "first_step": "Ask someone to use an app you like and listen to what feels easy or confusing.",
        "project": "Sketch and test a small redesign that makes one everyday digital task easier to understand.",
        "source_note": "Locally curated career overview; verify training and licensing requirements in your region.",
        "roadmap": [
            {"phase": "Explore", "duration": "Week 1", "items": ["Notice friction in an everyday app", "Learn the basics of user-centered design", "Interview one person about a simple task"]},
            {"phase": "Build foundations", "duration": "Weeks 2–4", "items": ["Sketch a simple user flow", "Practice wireframing", "Learn accessibility and usability basics"]},
            {"phase": "Make a project", "duration": "Weeks 5–8", "items": ["Redesign one small experience", "Test your prototype with a few people", "Show how feedback shaped your final design"]},
        ],
    },
    {
        "id": "teacher",
        "title": "Teacher & Learning Facilitator",
        "category": "Education & community",
        "icon": "✎",
        "description": "Help people build confidence and understanding through thoughtful learning experiences.",
        "dimensions": {"analytical": 0.4, "technology": 0.2, "creative": 0.5, "people": 1.0, "detail": 0.5, "practical": 0.4, "leadership": 0.6},
        "strengths": ["Patience and encouragement", "Explaining ideas clearly", "Planning for different needs"],
        "first_step": "Choose a topic you know and teach one small idea to someone else.",
        "project": "Create a short lesson for one learner, then revise it based on what they found clear.",
        "source_note": "Locally curated career overview; verify training and licensing requirements in your region.",
        "roadmap": [
            {"phase": "Explore", "duration": "Week 1", "items": ["Notice how different people learn", "Volunteer to explain a topic", "Talk to an educator about their work"]},
            {"phase": "Build foundations", "duration": "Weeks 2–4", "items": ["Practice breaking a topic into steps", "Explore inclusive teaching strategies", "Create a short lesson outline"]},
            {"phase": "Make a project", "duration": "Weeks 5–8", "items": ["Design a short lesson or learning guide", "Try it with a willing learner", "Reflect on what helped them understand"]},
        ],
    },
    {
        "id": "entrepreneur",
        "title": "Entrepreneur & Product Builder",
        "category": "Business & innovation",
        "icon": "↗",
        "description": "Spot unmet needs, test ideas, and bring people together to build something valuable.",
        "dimensions": {"analytical": 0.5, "technology": 0.4, "creative": 0.8, "people": 0.7, "detail": 0.3, "practical": 0.7, "leadership": 1.0},
        "strengths": ["Initiative and resilience", "Creative problem-solving", "Communicating a vision"],
        "first_step": "Ask three people about a small everyday problem they wish were easier.",
        "project": "Prototype a low-cost solution to one small problem and write down what user feedback changes.",
        "source_note": "Locally curated career overview; verify training and licensing requirements in your region.",
        "roadmap": [
            {"phase": "Explore", "duration": "Week 1", "items": ["Keep a list of problems you notice", "Talk to people who experience one problem", "Learn how a small business works"]},
            {"phase": "Build foundations", "duration": "Weeks 2–4", "items": ["Practice testing assumptions", "Sketch a simple solution", "Estimate basic costs and resources"]},
            {"phase": "Make a project", "duration": "Weeks 5–8", "items": ["Create a low-cost prototype", "Ask potential users for feedback", "Decide what to improve or test next"]},
        ],
    },
    {
        "id": "healthcare",
        "title": "Healthcare Professional",
        "category": "Health & wellbeing",
        "icon": "+",
        "description": "Support people's health and wellbeing through attentive, evidence-informed care.",
        "dimensions": {"analytical": 0.5, "technology": 0.2, "creative": 0.2, "people": 1.0, "detail": 0.8, "practical": 0.8, "leadership": 0.3},
        "strengths": ["Care and empathy", "Careful observation", "Commitment to learning"],
        "first_step": "Explore different healthcare roles and the training each one requires in your region.",
        "project": "Compare two healthcare roles and map their typical settings, training routes, and boundaries.",
        "source_note": "Locally curated career overview; verify training and licensing requirements in your region.",
        "roadmap": [
            {"phase": "Explore", "duration": "Week 1", "items": ["Compare several healthcare roles", "Read about local training pathways", "Reflect on the settings where you would like to work"]},
            {"phase": "Build foundations", "duration": "Weeks 2–4", "items": ["Explore introductory health science", "Learn about communication and care ethics", "Look for a reputable volunteer or shadowing opportunity"]},
            {"phase": "Make a project", "duration": "Weeks 5–8", "items": ["Create a learning plan for one role", "Speak with a qualified professional", "Check admission and licensing requirements"]},
        ],
    },
]

def make_career(career_id, title, category, icon, description, dimensions, strengths, first_step, project):
    return {
        "id": career_id,
        "title": title,
        "category": category,
        "icon": icon,
        "description": description,
        "dimensions": dimensions,
        "strengths": strengths,
        "first_step": first_step,
        "project": project,
        "source_note": "Locally curated career overview; verify training and licensing requirements in your region.",
        "roadmap": [
            {"phase": "Explore", "duration": "Week 1", "items": [first_step, f"Find two reliable descriptions of a day in the life of a {title}.", "Write down which responsibilities sound energizing and which need more research."]},
            {"phase": "Build foundations", "duration": "Weeks 2–4", "items": [f"Choose one beginner resource about {title} and complete its first lesson.", f"Practice a foundational skill used in {title}.", "Ask a teacher, adviser, or working professional what beginners often misunderstand."]},
            {"phase": "Make a project", "duration": "Weeks 5–8", "items": [project, "Save the work and explain your decisions in a short reflection.", "Use feedback to choose one specific next skill to practice."]},
        ],
    }


_MORE_CAREERS = [
    ("cybersecurity-analyst", "Cybersecurity Analyst", "Technology & engineering", "◈", "Help organizations protect systems by monitoring risks, investigating alerts, and improving security practices.", {"analytical": 1, "technology": 1, "detail": .8, "practical": .5, "communication": .4}, ["Careful investigation", "Systems thinking", "Responsible handling of sensitive information"], "Learn basic networking concepts and map how a familiar app protects an account.", "Create a defensive security checklist for a fictional small organization."),
    ("machine-learning-engineer", "Machine Learning Engineer", "Technology & data", "⌘", "Build and evaluate software that learns patterns from data to support useful, carefully tested products.", {"analytical": 1, "technology": 1, "science": .8, "detail": .7, "creative": .4}, ["Mathematical curiosity", "Programming persistence", "Thoughtful model evaluation"], "Explore a beginner Python lesson and explain the difference between training data and test data.", "Train a small model on a public, non-sensitive sample dataset and document its limitations."),
    ("cloud-engineer", "Cloud Engineer", "Technology & engineering", "☁", "Design and maintain the online infrastructure that lets digital services run reliably.", {"technology": 1, "analytical": .7, "practical": .7, "organization": .6, "detail": .6}, ["Infrastructure thinking", "Reliability mindset", "Systematic troubleshooting"], "Draw the basic components needed to host a simple website.", "Create a diagram of a sample app's cloud architecture and explain three reliability choices."),
    ("product-manager", "Product Manager", "Business & product", "◉", "Connect user needs, business goals, and engineering work to help a product team choose what to build.", {"leadership": .8, "communication": .9, "analytical": .7, "people": .7, "organization": .8}, ["Prioritization", "Listening to users", "Clear decision-making"], "Choose a product you use and write down one user problem it solves.", "Draft a one-page product brief with a target user, problem, proposed change, and success measure."),
    ("graphic-designer", "Graphic Designer", "Design & media", "✳", "Create visual communication for brands, publications, campaigns, and digital experiences.", {"creative": 1, "communication": .7, "technology": .5, "detail": .7}, ["Visual storytelling", "Iterating from feedback", "Design craft"], "Collect three examples of visual design and note what each communicates.", "Design a two-format poster and social graphic for a fictional community event."),
    ("writer-editor", "Writer & Editor", "Communication & media", "✎", "Research, shape, and refine writing so an audience can understand an idea and act on it.", {"communication": 1, "creative": .8, "analytical": .5, "detail": .8, "independence": .7}, ["Clear writing", "Research discipline", "Audience awareness"], "Rewrite a paragraph you recently read so a younger audience could understand it.", "Create a 500-word explainer, then edit it using a checklist for accuracy and clarity."),
    ("digital-marketer", "Digital Marketing Specialist", "Business & communication", "◎", "Help organizations reach the right audiences through thoughtful content, campaigns, and measurement.", {"communication": .8, "creative": .7, "analytical": .6, "technology": .5, "organization": .6}, ["Audience empathy", "Creative testing", "Interpreting campaign results"], "Compare how two organizations explain the same kind of service online.", "Plan a small campaign with a defined audience, message, channel, and measurable goal."),
    ("financial-analyst", "Financial Analyst", "Finance & business", "◌", "Use financial information and research to help people understand performance and make informed plans.", {"analytical": .9, "detail": .9, "technology": .5, "communication": .5, "organization": .6}, ["Numerical reasoning", "Careful research", "Explaining assumptions"], "Explore a simple sample budget and identify its three largest cost categories.", "Build a clearly labeled sample budget and write three evidence-based observations."),
    ("accountant", "Accountant", "Finance & business", "▤", "Keep financial records accurate, help organizations understand their obligations, and support sound decisions.", {"detail": 1, "analytical": .7, "organization": .8, "technology": .4, "service": .4}, ["Accuracy", "Consistency", "Ethical responsibility"], "Learn the purpose of an income statement, balance sheet, and cash-flow statement.", "Organize a fictional month's transactions into a simple categorized spreadsheet."),
    ("civil-engineer", "Civil Engineer", "Engineering & infrastructure", "⌂", "Plan and improve infrastructure such as buildings, transport, water systems, and public spaces.", {"science": .7, "analytical": .8, "practical": .8, "organization": .6, "environment": .5}, ["Applied mathematics", "Safety-first design", "Systems thinking"], "Notice a public structure and list the constraints its designers likely considered.", "Sketch an accessible, weather-aware redesign of a small public waiting area."),
    ("mechanical-engineer", "Mechanical Engineer", "Engineering & manufacturing", "⚙", "Design, test, and improve machines, products, and mechanical systems.", {"science": .8, "analytical": .8, "practical": .9, "technology": .6, "creative": .5}, ["Understanding how things work", "Prototyping", "Iterative testing"], "Take a safe household mechanism and diagram how its parts move together.", "Sketch and test a simple paper prototype that solves a small everyday problem."),
    ("environmental-scientist", "Environmental Scientist", "Science & sustainability", "❋", "Study environmental systems and help communities understand and reduce environmental impacts.", {"science": 1, "environment": 1, "analytical": .8, "communication": .6, "practical": .4}, ["Evidence-based observation", "Environmental stewardship", "Communicating findings"], "Pick one local environmental question and identify what evidence could answer it.", "Create a small observation log and summarize one pattern with its limitations."),
    ("research-scientist", "Research Scientist", "Science & research", "⚗", "Ask focused questions, design careful studies, and share evidence that advances understanding.", {"science": 1, "analytical": 1, "detail": .8, "independence": .6, "communication": .5}, ["Curiosity", "Careful methodology", "Honest interpretation"], "Read a beginner-friendly summary of one scientific study and identify its question.", "Design a safe, small observation study and document a question, method, and possible limitations."),
    ("psychologist", "Psychologist & Counselor", "Health & wellbeing", "☯", "Support mental wellbeing through listening, evidence-informed approaches, and appropriate professional training.", {"people": 1, "service": 1, "science": .6, "communication": .8, "detail": .5}, ["Empathetic listening", "Respect for boundaries", "Commitment to evidence"], "Compare the training requirements of two regulated helping professions in your region.", "Create a one-page overview of professional training and ethical boundaries for one role."),
    ("nurse", "Nurse", "Health & wellbeing", "✚", "Provide hands-on, coordinated care and help patients navigate health needs in varied settings.", {"service": 1, "people": .9, "science": .7, "detail": .8, "practical": .8, "communication": .7}, ["Compassionate care", "Attention to detail", "Calm teamwork"], "Research accredited nursing pathways and the kinds of placements they include.", "Create a comparison of two nursing settings and their typical day-to-day responsibilities."),
    ("physical-therapist", "Physical Therapist", "Health & movement", "↗", "Help people improve movement and daily function through assessment, education, and individualized practice.", {"service": .9, "people": .8, "science": .7, "practical": .8, "communication": .7}, ["Encouragement", "Applied anatomy", "Patient-centered planning"], "Explore how physical therapists support recovery in two different settings.", "Design a fictional, non-clinical activity-tracking sheet and explain how it supports goal-setting."),
    ("lawyer", "Lawyer & Legal Researcher", "Law & public service", "§", "Research rules, analyze arguments, and help people or organizations understand legal options and obligations.", {"analytical": 1, "communication": .9, "detail": .8, "people": .6, "service": .5}, ["Structured argument", "Close reading", "Professional ethics"], "Find out what accredited legal training and licensing involve in your region.", "Compare two publicly available policy arguments and summarize their evidence without giving legal advice."),
    ("human-resources-specialist", "Human Resources Specialist", "People & organizations", "♧", "Help workplaces recruit, support, and develop people while handling processes consistently and fairly.", {"people": .9, "communication": .8, "organization": .8, "detail": .7, "service": .6}, ["Discretion", "Clear communication", "Fair process"], "Map the steps a candidate might experience when applying for a role.", "Draft an inclusive sample onboarding checklist for a fictional new team member."),
    ("project-manager", "Project Manager", "Business & operations", "◷", "Coordinate people, timelines, risks, and decisions so a team can deliver a defined outcome.", {"organization": 1, "communication": .8, "leadership": .8, "analytical": .6, "people": .6}, ["Planning", "Facilitating collaboration", "Managing changing priorities"], "Break a simple school or community project into milestones and owners.", "Create a one-page plan with a goal, three milestones, risks, and next actions."),
    ("sales-consultant", "Sales Consultant", "Business & relationships", "↗", "Understand customer needs and explain relevant products or services in a transparent, helpful way.", {"communication": .9, "people": .8, "entrepreneurship": .6, "organization": .5, "leadership": .4}, ["Listening", "Building trust", "Explaining value honestly"], "Compare two products and list the needs each is best suited to support.", "Write a customer conversation guide with discovery questions and an honest product summary."),
    ("social-worker", "Social Worker", "Community & public service", "♡", "Connect people with support and advocate for wellbeing while respecting dignity and professional boundaries.", {"service": 1, "people": 1, "communication": .8, "organization": .6, "leadership": .4}, ["Empathy", "Advocacy", "Respect for privacy"], "Explore social work training and role boundaries in a setting that interests you.", "Map local public support services for a fictional scenario using published, non-sensitive information."),
    ("electrician", "Electrician & Skilled Trades Professional", "Skilled trades & technology", "ϟ", "Install, inspect, and repair practical systems through hands-on work, technical knowledge, and safety procedures.", {"practical": 1, "technology": .6, "detail": .9, "analytical": .5, "independence": .6}, ["Hands-on problem-solving", "Safety awareness", "Precision"], "Research licensed training pathways and safety requirements in your area.", "Draw a labeled, non-operational diagram of a familiar system and identify the relevant safety checks."),
    ("chef", "Chef & Culinary Professional", "Food & hospitality", "♨", "Plan and prepare food while balancing technique, timing, safety, and the needs of guests or teams.", {"creative": .7, "practical": 1, "organization": .8, "people": .6, "detail": .6}, ["Creative practice", "Time management", "Food safety"], "Compare the responsibilities of two kitchen roles in different settings.", "Plan a simple menu with a prep timeline, ingredient list, and food-safety reminders."),
    ("agricultural-scientist", "Agricultural & Food Scientist", "Science & food systems", "❀", "Improve food production and quality by applying science to crops, animals, resources, and supply systems.", {"science": .9, "environment": .8, "analytical": .7, "practical": .6, "detail": .6}, ["Systems thinking", "Evidence-led experiments", "Sustainable resource use"], "Trace one everyday food from production to the table and note questions along the way.", "Compare two published approaches to reducing waste in a fictional food-growing scenario."),
    ("policy-analyst", "Public Policy Analyst", "Government & public service", "▧", "Research public issues and compare possible approaches to help decision-makers understand trade-offs.", {"analytical": .9, "communication": .8, "service": .6, "organization": .5, "leadership": .4}, ["Evidence synthesis", "Balanced reasoning", "Clear writing"], "Choose a public issue and list who is affected and what evidence would help.", "Write a one-page neutral policy brief describing a problem, two options, and trade-offs."),
    ("game-designer", "Game Designer", "Design & interactive media", "◇", "Shape the rules, stories, and player experiences that make games engaging and understandable.", {"creative": 1, "technology": .5, "analytical": .7, "communication": .6, "people": .4}, ["Systems creativity", "Playtesting", "Audience empathy"], "Analyze one game mechanic and describe what makes it satisfying or confusing.", "Create a paper prototype with clear rules and test one round with a willing participant."),
]

CAREERS.extend(
    make_career(*career_data)
    for career_data in _MORE_CAREERS
)

CAREER_TASKS = [
    {
        "id": "career-snapshot",
        "focus": "communication",
        "title": "Build a career reality-check",
        "duration": "25 min",
        "icon": "⌕",
        "description": "Research the day-to-day work of a {title} using two reliable career or professional sources.",
        "steps": ["Write down three recurring responsibilities.", "Note one work setting and one qualification or training route.", "Record one part that attracts you and one question you still have."],
        "deliverable": "A 5-bullet career snapshot with sources and one open question.",
    },
    {
        "id": "strengths-audit",
        "focus": "independence",
        "title": "Connect your strengths to the work",
        "duration": "20 min",
        "icon": "◉",
        "description": "Compare what a {title} does with skills you have already used in school, work, hobbies, or volunteering.",
        "steps": ["List two strengths and a real example for each.", "Choose one important skill you want to develop.", "Name one low-risk way to practice that skill this week."],
        "deliverable": "A three-row strengths table with evidence and one practice goal.",
    },
    {
        "id": "starter-project",
        "focus": "creative",
        "title": "Complete a tiny career project",
        "duration": "45 min",
        "icon": "✦",
        "description": "{project}",
        "steps": ["Spend five minutes defining the audience and the goal.", "Work for 30 focused minutes; save a draft or photo of the result.", "Spend ten minutes noting what you tried and what you would change."],
        "deliverable": "One small saved artifact plus a 3-sentence reflection.",
    },
    {
        "id": "learning-sprint",
        "focus": "analytical",
        "title": "Finish one focused learning sprint",
        "duration": "30 min",
        "icon": "▤",
        "description": "Choose one beginner lesson related to {title}; do not try to learn an entire subject in one sitting.",
        "steps": ["Select a reputable introductory lesson that takes 20 minutes or less.", "Complete it and write three key takeaways in your own words.", "Write one question you would ask a teacher or practitioner."],
        "deliverable": "Three takeaways and one next question in your learning notes.",
    },
    {
        "id": "conversation-plan",
        "focus": "people",
        "title": "Prepare a career conversation",
        "duration": "20 min",
        "icon": "☏",
        "description": "Prepare to learn from someone familiar with {title}; the goal is insight, not asking them for a job.",
        "steps": ["Write five open questions about their typical week, training, and challenges.", "Draft a polite 3-sentence request for a 15-minute conversation.", "Identify one teacher, adviser, community contact, or public event where you could ask."],
        "deliverable": "Five respectful questions and a short conversation request draft.",
    },
    {
        "id": "portfolio-reflection",
        "focus": "organization",
        "title": "Document what you learned",
        "duration": "15 min",
        "icon": "▣",
        "description": "Capture progress on your {title} exploration while the details are still fresh.",
        "steps": ["Save a link, image, note, or draft from one activity.", "Write what you set out to do and what you actually completed.", "Choose one specific adjustment or next step based on what you learned."],
        "deliverable": "A dated portfolio note with an artifact and a concrete next step.",
    },
    {
        "id": "role-requirements",
        "focus": "detail",
        "title": "Check the real entry requirements",
        "duration": "25 min",
        "icon": "⌑",
        "description": "Check a current, reliable local source for common entry requirements for a {title}.",
        "steps": ["Find two current job or training descriptions.", "Separate required qualifications from preferred experience.", "Write down one local requirement you need to verify with an adviser."],
        "deliverable": "A short, sourced checklist of entry requirements and one question.",
    },
    {
        "id": "skill-gap-map",
        "focus": "analytical",
        "title": "Map one skill gap into practice",
        "duration": "20 min",
        "icon": "⌗",
        "description": "Choose one important beginner skill used in {title} and break it into a practiceable next step.",
        "steps": ["Find a skill mentioned in two role descriptions.", "Rate your current confidence from 1 to 5 and name evidence for the rating.", "Choose one exercise that would help you move up one confidence point."],
        "deliverable": "One skill, an honest baseline, and a specific practice exercise.",
    },
    {
        "id": "workday-map",
        "focus": "organization",
        "title": "Sketch a realistic workday",
        "duration": "20 min",
        "icon": "◷",
        "description": "Use current descriptions of {title} to sketch how one typical day might be divided.",
        "steps": ["List three common responsibilities from reliable sources.", "Arrange them into a possible morning, afternoon, and collaboration block.", "Mark which assumptions still need checking with a real practitioner."],
        "deliverable": "A one-page sample workday with sources and assumptions labeled.",
    },
    {
        "id": "explain-a-concept",
        "focus": "communication",
        "title": "Teach back one career concept",
        "duration": "20 min",
        "icon": "❞",
        "description": "Learn one beginner concept used in {title} and explain it to someone new to the subject.",
        "steps": ["Choose a concept from a reputable beginner resource.", "Explain it in five sentences without copying the source.", "Check the explanation against the source and correct one unclear detail."],
        "deliverable": "A checked five-sentence explanation and one cited learning source.",
    },
    {
        "id": "compare-career-paths",
        "focus": "analytical",
        "title": "Compare two nearby career paths",
        "duration": "25 min",
        "icon": "⇄",
        "description": "Compare {title} with a related role that shares some skills but has different daily work.",
        "steps": ["Find one current description for each role.", "Compare responsibilities, setting, and training in a three-row table.", "Record one difference that changes your interest and one question to investigate."],
        "deliverable": "A side-by-side role comparison with sources and a new question.",
    },
    {
        "id": "goal-setting",
        "focus": "leadership",
        "title": "Set a one-week career experiment",
        "duration": "15 min",
        "icon": "◎",
        "description": "Plan a small experiment that helps you learn whether a part of {title} suits you.",
        "steps": ["Write one question you want your experiment to answer.", "Choose an action that takes no more than one hour this week.", "Set a day to try it and define what you will write down afterward."],
        "deliverable": "A dated one-week experiment with a question and a reflection plan.",
    },
    {
        "id": "source-check",
        "focus": "detail",
        "title": "Verify a career fact before you act",
        "duration": "15 min",
        "icon": "⌕",
        "description": "Choose one claim about becoming a {title} and verify it using a current official or professional source.",
        "steps": ["Write one claim about training, licensing, or job outlook.", "Find its original source, such as a regulator, school, or professional body.", "Note the publication or update date and any location-specific limits."],
        "deliverable": "One checked fact, its dated source, and a note on where it applies.",
    },
    {
        "id": "practice-interview",
        "focus": "communication",
        "title": "Practice a career story",
        "duration": "20 min",
        "icon": "◖",
        "description": "Practice explaining a real experience that demonstrates a skill relevant to {title}.",
        "steps": ["Pick a school, work, hobby, or volunteering example.", "Write the situation, your action, and the result in three short notes.", "Say the story aloud in under one minute and adjust one unclear sentence."],
        "deliverable": "A one-minute practice story grounded in a real example.",
    },
]

DIMENSION_LABELS = {
    "analytical": "analytical thinking",
    "technology": "technology",
    "creative": "creative work",
    "people": "working with people",
    "detail": "attention to detail",
    "practical": "hands-on work",
    "leadership": "leadership",
    "science": "science and investigation",
    "communication": "communication",
    "organization": "planning and organization",
    "environment": "environmental impact",
    "service": "service and wellbeing",
    "independence": "independent work",
    "entrepreneurship": "building new ideas",
}


def tasks_for_career(career):
    title = career["title"] if career else "a career you are exploring"
    project = (
        career.get("project", career["first_step"])
        if career
        else "Create a one-page map of the people and steps involved in a skill or service that interests you."
    )
    return [
        {
            **task,
            "description": task["description"].format(
                title=title, project=project
            ),
        }
        for task in CAREER_TASKS
    ]


def daily_tasks_for_career(career, user_id, plan_date, assessment_scores=None, recent_task_ids=()):
    """Rank and select a stable three-task daily plan for this user and local calendar date."""
    tasks = tasks_for_career(career)
    if not tasks:
        return []
    assessment_scores = assessment_scores or {}
    recent_counts = {}
    for task_id in recent_task_ids:
        recent_counts[task_id] = recent_counts.get(task_id, 0) + 1
    career_dimensions = career["dimensions"] if career else {}
    rng = random.Random(f"{user_id}:{plan_date.isoformat()}")
    scored_tasks = []
    for task in tasks:
        focus = task["focus"]
        career_fit = career_dimensions.get(focus, 0.35)
        personal_fit = assessment_scores.get(focus, 3) / 5
        recency_penalty = min(recent_counts.get(task["id"], 0) * 0.18, 0.54)
        variation = rng.random() * 0.14
        score = career_fit * 0.6 + personal_fit * 0.4 - recency_penalty + variation
        scored_tasks.append((score, task["id"], task))
    selected = []
    selected_focus = set()
    remaining = sorted(scored_tasks, key=lambda row: (row[0], row[1]), reverse=True)
    if remaining:
        daily_offset = (plan_date.toordinal() + user_id) % len(remaining)
        remaining = remaining[daily_offset:] + remaining[:daily_offset]
    while remaining and len(selected) < 3:
        next_index = next(
            (index for index, row in enumerate(remaining) if row[2]["focus"] not in selected_focus),
            0,
        )
        _, _, task = remaining.pop(next_index)
        selected.append(task)
        selected_focus.add(task["focus"])
    return selected


def video_recommendations(career):
    """Return progressive YouTube search recommendations, not unverified video URLs."""
    from urllib.parse import quote_plus

    career_title = career["title"] if career else "career exploration and work skills"
    topics = [
        ("Beginner", "A day in the life and career introduction", "day in the life beginner guide"),
        ("Beginner", "Core concepts and a beginner learning path", "beginner fundamentals learning roadmap tutorial"),
        ("Intermediate", "Follow a guided practical project", "guided practical project tutorial with explanation"),
        ("Intermediate", "Explore a professional workflow or case study", "intermediate skills workflow case study"),
        ("Advanced", "Study an advanced project and specialization", "advanced specialization real-world project walkthrough"),
        ("Advanced", "Hear expert perspectives on current challenges", "industry expert trends challenges professional discussion"),
    ]
    return [
        {
            "level": level,
            "title": title,
            "query": f"{career_title} {topic}",
            "url": f"https://www.youtube.com/results?search_query={quote_plus(f'{career_title} {topic}')}",
        }
        for level, title, topic in topics
    ]
