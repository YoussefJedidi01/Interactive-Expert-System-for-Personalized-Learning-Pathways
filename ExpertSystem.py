import tkinter as tk
from tkinter import messagebox
import webbrowser


class DynamicExpertSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Système Expert d'apprentissage ")
        self.root.geometry("800x600")
        self.root.resizable(False, False)

        # Initialisation des variables
        self.user_data = {}
        self.current_question_index = 0
        self.questions = []
        self.recommendation = ""

        # Initialisation de l'interface
        self.question_label = tk.Label(root, text="", font=("Arial", 16), wraplength=750)
        self.question_label.pack(pady=20)

        self.answer_var = tk.StringVar()
        self.answer_entry = None  # Sera ajouté dynamiquement
        self.options_buttons = []

        self.next_button = tk.Button(
            root, text="Suivant", font=("Arial", 12), bg="#4CAF50", fg="white", command=self.next_question
        )
        self.next_button.pack(pady=20)

        # Gérer l'événement "Entrée"
        root.bind("<Return>", lambda event: self.next_question())

        # Ajout de la signature
        self.signature_label = tk.Label(
            root,
            text="Done by: Youssef Jedidi & Iheb Aouini",
            font=("Arial", 10),
            fg="gray",
        )
        self.signature_label.pack(side="bottom", pady=10)

        # Initialiser les questions et démarrer
        self.init_questions()
        self.show_question()

    def init_questions(self):
        """Initialise les questions et leurs logiques."""
        self.questions = [
            {"text": "Quel est votre niveau en programmation ?", "type": "options", "options": ["Débutant", "Intermédiaire", "Avancé"], "key": "level"},
            {"text": "Quel est votre objectif d'apprentissage ?", "type": "options", "options": ["Web", "Machine Learning", "DevOps", "Cloud", "Cybersécurité", "Data Science", "Autre"], "key": "goal"},
            {"text": "Si 'Autre', précisez votre domaine d'apprentissage.", "type": "input", "key": "custom_goal", "condition": lambda data: data.get("goal") == "Autre"},
            {"text": "Combien d'heures par semaine pouvez-vous consacrer à l'apprentissage ? (nombre entier)", "type": "input", "key": "available_time"},
            {"text": "Préférez-vous un apprentissage ?", "type": "options", "options": ["Théorique", "Pratique", "Mixte"], "key": "preference"},
            {"text": "Avez-vous une expérience professionnelle dans ce domaine ?", "type": "options", "options": ["Oui", "Non"], "key": "experience"},
            {"text": "Quelle est votre langue préférée pour les ressources ?", "type": "options", "options": ["Français", "Anglais", "Autre"], "key": "language"},
            {"text": "Préférez-vous travailler seul ou en équipe ?", "type": "options", "options": ["Seul", "En équipe"], "key": "work_preference"},
            {"text": "Quel est votre objectif principal ?", "type": "options", "options": ["Trouver un emploi", "Créer un projet personnel", "Améliorer mes compétences"], "key": "main_goal"},
            {"text": "Quel type de ressources préférez-vous ?", "type": "options", "options": ["Vidéo", "Livres", "Cours en ligne", "Projets pratiques"], "key": "resource_preference"},
        ]

    def show_question(self):
        """Affiche la question actuelle en fonction de l'index."""
        # Vider l'écran
        self.answer_var.set("")
        self.question_label.config(text="")
        if self.answer_entry:
            self.answer_entry.pack_forget()
        for button in self.options_buttons:
            button.pack_forget()
        self.options_buttons = []

        # Récupérer la question actuelle
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]

            # Vérifier les conditions (si la question doit être posée)
            if "condition" in question and not question["condition"](self.user_data):
                self.current_question_index += 1
                self.show_question()
                return

            self.question_label.config(text=question["text"])

            # Afficher les options
            if question["type"] == "options":
                for option in question["options"]:
                    button = tk.Radiobutton(
                        self.root,
                        text=option,
                        variable=self.answer_var,
                        value=option,
                        font=("Arial", 12),
                    )
                    button.pack(anchor="w", padx=20)
                    self.options_buttons.append(button)

            # Champ d'entrée
            elif question["type"] == "input":
                self.answer_entry = tk.Entry(self.root, textvariable=self.answer_var, font=("Arial", 12), width=40)
                self.answer_entry.pack(pady=10)

        else:
            # Toutes les questions ont été posées
            self.generate_recommendation()

    def next_question(self):
        """Passe à la question suivante après avoir enregistré la réponse."""
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            answer = self.answer_var.get().strip()

            # Validation des réponses
            if not answer:
                messagebox.showerror("Erreur", "Veuillez répondre à la question avant de continuer.")
                return
            if question["type"] == "input" and question["key"] == "available_time":
                try:
                    answer = int(answer)  # Conversion en entier pour les heures
                except ValueError:
                    messagebox.showerror("Erreur", "Veuillez entrer un nombre valide pour les heures.")
                    return

            # Sauvegarder la réponse
            self.user_data[question["key"]] = answer

        # Passer à la question suivante
        self.current_question_index += 1
        self.show_question()

    def open_link(self, url):
        """Ouvre un lien dans le navigateur."""
        webbrowser.open_new_tab(url)

    def generate_recommendation(self):
        """Génère une recommandation finale basée sur les réponses."""
        self.next_button.pack_forget()
        self.question_label.config(text="Recommandation personnalisée :")

        # Récupérer les réponses de l'utilisateur
        goal = self.user_data.get("goal", "")
        custom_goal = self.user_data.get("custom_goal", "") if goal == "Autre" else goal
        level = self.user_data.get("level", "")
        time = self.user_data.get("available_time", 0)
        experience = self.user_data.get("experience", "")
        work_preference = self.user_data.get("work_preference", "")

        if goal == "Autre" and not custom_goal:
        	messagebox.showerror("Erreur", "Veuillez préciser votre domaine d'apprentissage.")
        	return  # Arrête l'exécution si custom_goal est vide



        # Liste des recommandations
        recommendations = []

        google_search_url = f'https://www.google.com/search?q="{custom_goal}+article"'
        youtube_search_url = f'https://www.youtube.com/results?search_query={custom_goal}'



        if goal == "Web" and level == "Débutant" and work_preference == "Seul":
            recommendations.append(
                "Commencez avec HTML, CSS et JavaScript. "
                "Apprenez sur FreeCodeCamp et créez un portfolio. "
                "Explorez des références fiables comme MDN Web Docs. "
                "Participez à des forums pour poser des questions. "
                "Travaillez sur des projets comme un site de portfolio. "
                "Prenez le temps d'expérimenter les concepts."

            )
        if goal == "Web" and level == "Débutant" and work_preference == "En équipe":
            recommendations.append(
                "Apprenez HTML, CSS et JavaScript avec des amis ou en groupe. "
                "Participez à des projets collaboratifs sur GitHub. "
                "Créez des projets simples, comme un site pour une petite entreprise. "
                "Utilisez des ressources interactives comme Codecademy. "
                "Explorez les outils de collaboration comme Git. "
                "Posez vos questions sur des forums comme Stack Overflow."

            )
        if goal == "Web" and level == "Intermédiaire" and experience == "Non":
            recommendations.append(
                "Explorez des frameworks comme React ou Vue.js. "
                "Travaillez sur des projets open-source pour acquérir de l'expérience. "
                "Développez un site complet en utilisant Node.js pour le backend. "
                "Utilisez Docker pour gérer les environnements. "
                "Créez un blog technique pour partager vos connaissances. "
                "Apprenez à déployer des applications avec Netlify ou Vercel."

            )
        if goal == "Web" and level == "Avancé" and experience == "Oui":
            recommendations.append(
                "Maîtrisez les concepts avancés comme SSR et CSR avec Next.js. "
                "Explorez les architectures headless CMS. "
                "Participez à des projets complexes avec des bases de données comme MongoDB. "
                "Automatisez les tests unitaires avec Jest. "
                "Collaborez avec des équipes via GitHub et Jira. "
                "Rédigez des articles techniques pour renforcer votre portfolio."

            )

        # Règles pour Machine Learning
        if goal == "Machine Learning" and level == "Débutant" and time <= 5:
            recommendations.append(
                "Apprenez les bases de Python et les bibliothèques comme Pandas et NumPy. "
                "Explorez des tutoriels simples pour apprendre la régression linéaire. "
                "Participez à des concours simples sur Kaggle. "
                "Lisez des articles ou des livres comme 'Python for Data Analysis'. "
                "Visualisez vos données avec Matplotlib. "
                "Créez un projet simple comme prédire les prix d'une maison."

            )
        if goal == "Machine Learning" and level == "Intermédiaire" and time > 10:
            recommendations.append(
                "Plongez dans des algorithmes avancés comme les réseaux de neurones. "
                "Apprenez TensorFlow et PyTorch pour créer vos modèles. "
                "Travaillez avec des datasets sur UCI Repository ou Kaggle. "
                "Participez à des compétitions pour tester vos compétences. "
                "Explorez les concepts de traitement du langage naturel (NLP). "
                "Apprenez à déployer vos modèles sur des serveurs en production."

            )
        if goal == "Machine Learning" and level == "Avancé" and experience == "Oui":
            recommendations.append(
                "Maîtrisez l'optimisation des hyperparamètres pour améliorer vos modèles. "
                "Explorez les architectures avancées comme les transformers. "
                "Participez à des projets industriels ou académiques pour enrichir votre expérience. "
                "Publiez des articles techniques sur Medium ou GitHub. "
                "Explorez les solutions de déploiement comme TensorFlow Serving. "
                "Collaborez avec des équipes pour résoudre des problèmes complexes."

            )

        # Règles pour Cybersécurité
        if goal == "Cybersécurité" and level == "Débutant" and work_preference == "Seul":
            recommendations.append(
                "Apprenez les bases de la cybersécurité sur des plateformes comme TryHackMe. "
                "Explorez Wireshark pour analyser le trafic réseau. "
                "Participez à des exercices de capture de drapeaux (CTFs). "
                "Apprenez à identifier les vulnérabilités avec OWASP. "
                "Créez un blog pour partager vos découvertes en sécurité. "
                "Familiarisez-vous avec des outils comme Burp Suite et Nmap."

            )
        if goal == "Cybersécurité" and level == "Intermédiaire" and time > 10:
            recommendations.append(
                "Apprenez l'exploitation avancée des vulnérabilités avec Metasploit. "
                "Explorez les concepts de sécurité dans le cloud. "
                "Participez à des challenges CTF pour perfectionner vos compétences. "
                "Travaillez sur des projets comme sécuriser une application web. "
                "Apprenez à effectuer des audits de sécurité complets. "
                "Explorez des certifications comme CEH ou CISSP."

            )

        # Règles pour Data Science
        if goal == "Data Science" and level == "Débutant":
            recommendations.append(
                "Apprenez Python avec un focus sur les bibliothèques comme Pandas et NumPy. "
                "Explorez des datasets simples sur Kaggle. "
                "Apprenez à visualiser vos données avec Seaborn et Matplotlib. "
                "Participez à des tutoriels interactifs pour la manipulation des données. "
                "Travaillez sur des projets comme l'analyse de ventes. "
                "Familiarisez-vous avec les concepts de machine learning pour débutants."

            )
        if goal == "Data Science" and level == "Intermédiaire":
            recommendations.append(
                "Travaillez sur des projets plus complexes, comme la prévision des ventes. "
                "Apprenez à utiliser Scikit-learn pour implémenter des modèles prédictifs. "
                "Explorez les techniques d'analyse exploratoire approfondie. "
                "Participez à des compétitions de science des données sur Kaggle. "
                "Apprenez les bases des réseaux neuronaux pour l'analyse avancée. "
                "Créez un blog pour partager vos analyses et découvertes."

            )
        if goal == "Data Science" and level == "Avancé":
            recommendations.append(
                "Explorez des frameworks avancés comme TensorFlow ou PyTorch. "
                "Apprenez à déployer vos modèles en production avec Docker. "
                "Travaillez sur des projets d'analyse prédictive à grande échelle. "
                "Collaborez avec des équipes pour travailler sur des datasets complexes. "
                "Explorez des concepts avancés comme le traitement des séries temporelles. "
                "Participez à des conférences ou meetups pour échanger vos idées."

 )
        if goal == "Cloud" and level == "Débutant" and work_preference == "Seul":
            recommendations.append(
                "Apprenez les bases des services cloud comme AWS ou Azure. "
                "Familiarisez-vous avec les concepts d'IaaS, PaaS, et SaaS. "
                "Suivez des tutoriels interactifs sur AWS Free Tier. "
                "Explorez des outils comme Terraform pour l'automatisation. "
                "Créez un projet simple, comme héberger un site sur S3. "
                "Participez à des formations gratuites proposées par AWS ou Azure."

            )
        if goal == "Cloud" and level == "Intermédiaire" and work_preference == "En équipe":
            recommendations.append(
                "Apprenez les principes de la conception multi-cloud. "
                "Explorez Kubernetes pour la gestion des conteneurs. "
                "Utilisez Terraform pour automatiser vos infrastructures. "
                "Collaborez sur des projets de déploiement d'applications cloud. "
                "Obtenez des certifications comme AWS Solutions Architect. "
                "Participez à des hackathons cloud pour des cas pratiques."

            )
        if goal == "Cloud" and level == "Avancé" and experience == "Oui":
            recommendations.append(
                "Maîtrisez les concepts de microservices et de serverless. "
                "Explorez des frameworks avancés comme AWS Lambda ou Azure Functions. "
                "Implémentez des solutions hybrides ou multi-clouds complexes. "
                "Contribuez à des projets open-source liés à l'infrastructure cloud. "
                "Apprenez à gérer la sécurité dans le cloud avec des outils comme IAM. "
                "Partagez vos connaissances via des blogs ou des conférences techniques."

            )

        # Règles pour DevOps
        if goal == "DevOps" and level == "Débutant" and time <= 5:
            recommendations.append(
                "Commencez avec les bases de Git et GitHub pour la gestion du code. "
                "Apprenez à utiliser Docker pour créer et gérer des conteneurs. "
                "Explorez les principes CI/CD avec des outils comme GitHub Actions. "
                "Travaillez sur de petits projets pour automatiser des tâches simples. "
                "Suivez des tutoriels interactifs sur les bases de DevOps. "
                "Lisez des articles sur les bonnes pratiques en DevOps."

            )
        if goal == "DevOps" and level == "Intermédiaire" and experience == "Non":
            recommendations.append(
                "Apprenez à configurer des pipelines CI/CD avec Jenkins ou GitLab CI. "
                "Explorez Ansible pour l'automatisation de la configuration. "
                "Collaborez sur des projets open-source DevOps pour gagner en expérience. "
                "Travaillez sur des projets personnels pour intégrer des outils comme Docker et Kubernetes. "
                "Participez à des formations avancées sur Udemy ou Pluralsight. "
                "Créez des scripts d'automatisation pour simplifier vos workflows."

            )
        if goal == "DevOps" and level == "Avancé" and experience == "Oui":
            recommendations.append(
                "Maîtrisez les concepts avancés de Kubernetes, comme les opérateurs et l'autoscaling. "
                "Développez des pipelines CI/CD complexes pour des projets multi-environnements. "
                "Explorez les outils d'infrastructure comme Terraform ou Pulumi. "
                "Contribuez à des projets DevOps à grande échelle dans votre entreprise. "
                "Optimisez les performances avec le monitoring avancé (Prometheus, Grafana). "
                "Participez à des conférences techniques sur DevOps pour partager vos connaissances."

            )

        # Règles pour Autre
        if goal == "Autre" and self.user_data.get("custom_goal") and level == "Débutant":
            recommendations.append(
                f"Pour le domaine '{self.user_data['custom_goal']}', commencez par explorer des tutoriels interactifs. "
                "Recherchez des cours en ligne spécifiques à ce domaine sur Coursera ou Udemy. "
                "Rejoignez des communautés en ligne pour poser vos questions. "
                "Créez un projet pratique pour appliquer vos nouvelles compétences. "
                "Lisez des blogs et articles pour approfondir vos connaissances. "
                "Participez à des événements ou ateliers liés à ce domaine."

            )
        if goal == "Autre" and self.user_data.get("custom_goal") and level == "Intermédiaire":
            recommendations.append(
                f"Dans le domaine '{self.user_data['custom_goal']}', travaillez sur des projets complexes. "
                "Explorez des frameworks ou outils spécifiques pour ce domaine. "
                "Participez à des hackathons ou compétitions pour tester vos compétences. "
                "Lisez des livres ou suivez des webinaires sur les dernières avancées. "
                "Contribuez à des projets open-source pour enrichir votre expérience. "
                "Publiez vos travaux ou découvertes dans des blogs techniques."

            )
        if goal == "Autre" and self.user_data.get("custom_goal") and level == "Avancé":
            recommendations.append(
                f"Dans le domaine '{self.user_data['custom_goal']}', explorez les concepts avancés. "
                "Rejoignez des équipes ou communautés professionnelles pour collaborer. "
                "Travaillez sur des projets industriels ou académiques. "
                "Publiez des articles ou participez à des conférences dans ce domaine. "
                "Explorez des solutions innovantes pour résoudre des problèmes complexes. "
                "Continuez à apprendre et à expérimenter pour rester à jour."

            )

        # Règles pour Cybersécurité avancée
        if goal == "Cybersécurité" and level == "Avancé" and experience == "Oui":
            recommendations.append(
                "Apprenez à réaliser des tests d'intrusion avancés sur des environnements complexes. "
                "Explorez les concepts de sécurité dans le cloud et la protection des conteneurs. "
                "Contribuez à des projets de recherche en cybersécurité. "
                "Travaillez sur des certifications comme OSCP ou CISSP pour valider vos compétences. "
                "Participez à des forums et conférences pour échanger des idées avec d'autres experts. "
                "Développez vos propres outils ou frameworks de sécurité."

            )

        # Règles pour Data Science avancée
        if goal == "Data Science" and level == "Avancé" and work_preference == "En équipe":
            recommendations.append(
                "Collaborez sur des projets en équipe pour résoudre des problèmes industriels. "
                "Utilisez des outils avancés comme Apache Spark pour le big data. "
                "Explorez les techniques de deep learning avec TensorFlow ou PyTorch. "
                "Apprenez à déployer des pipelines de données automatisés. "
                "Participez à des hackathons de science des données pour tester vos compétences. "
                "Publiez des articles sur vos découvertes ou méthodologies."

            )
        # Si aucune règle ne correspond
        if not recommendations:
            recommendations.append(
                "Nous avons constaté que vos besoins spécifiques ne correspondent pas à nos règles définies. "
                "Cependant, voici une stratégie générale pour maximiser votre apprentissage : "
                "1. Identifiez les compétences fondamentales nécessaires pour votre domaine cible et commencez par là. "
                "2. Trouvez des tutoriels interactifs ou des cours en ligne gratuits ou payants sur des plateformes comme Coursera, Udemy ou OpenClassrooms. "
                "3. Créez un projet personnel pour appliquer directement ce que vous apprenez. "
                "4. Rejoignez des communautés en ligne (comme Reddit, Discord ou LinkedIn) pour poser des questions et échanger avec d'autres apprenants. "
                "5. Consultez régulièrement des blogs ou des chaînes YouTube spécialisées pour rester à jour sur les dernières tendances. "
                "6. Enfin, prenez le temps de réfléchir à vos progrès et ajustez votre plan d'apprentissage au besoin."

            )

       # Combiner les recommandations
        self.recommendation = "\n\n".join(recommendations)
        self.display_recommendation(self.recommendation, google_search_url, youtube_search_url)

    def display_recommendation(self, text, google_link, youtube_link):
        """Affiche la recommandation avec des liens cliquables."""
        self.question_label.pack_forget()

        # Affichage du texte de recommandation
        label = tk.Label(self.root, text=text, font=("Arial", 12), wraplength=750, justify="left")
        label.pack()

        # Affichage des liens cliquables
        link_google = tk.Label(self.root, text="Articles sur Google", fg="blue", cursor="hand2", font=("Arial", 12, "underline"))
        link_google.pack()
        link_google.bind("<Button-1>", lambda e: self.open_link(google_link))

        link_youtube = tk.Label(self.root, text="Vidéos sur YouTube", fg="blue", cursor="hand2", font=("Arial", 12, "underline"))
        link_youtube.pack()
        link_youtube.bind("<Button-1>", lambda e: self.open_link(youtube_link))


# Démarrage de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = DynamicExpertSystem(root)
    root.mainloop()
