import React from 'react';
import { Link } from 'react-router-dom';
import { GitFork, MessageSquare, BookOpen, Sparkles } from 'lucide-react';
import { Footer } from '../../components/organisms/Footer/Footer';
import styles from './LandingPage.module.css';

const FEATURES = [
  {
    icon: MessageSquare,
    title: 'Chat con IA',
    description: 'Haz preguntas sobre la UMSS y recibe respuestas instantáneas',
  },
  {
    icon: BookOpen,
    title: 'Bolsa de Trabajo',
    description: 'Explora oportunidades laborales y becas disponibles',
  },
  {
    icon: Sparkles,
    title: 'Noticias',
    description: 'Mantente informado con las últimas novedades universitarias',
  },
];

export const LandingPage: React.FC = () => {
  return (
    <div className={styles.page}>
      <nav className={styles.nav}>
        <span className={styles.logo}>Botcachino</span>
        <a href="https://github.com/willypaz243/botcachino_monorepo" target="_blank" rel="noopener noreferrer" className={styles.navLink}>
          <GitFork size={18} />
          <span>GitHub</span>
        </a>
      </nav>

      <header className={styles.hero}>
        <h1 className={styles.heroTitle}>
          Tu asistente inteligente de la{' '}
          <span className={styles.highlight}>UMSS</span>
        </h1>
        <p className={styles.heroSubtitle}>
          Botcachino te ayuda a encontrar información sobre la Universidad Mayor de San Simón,
          bolsas de trabajo, becas y noticias relevantes.
        </p>
        <Link to="/agent" className={styles.ctaButton}>
          <MessageSquare size={20} />
          Comenzar a chatear
        </Link>
      </header>

      <section className={styles.features}>
        {FEATURES.map((feature) => (
          <div key={feature.title} className={styles.featureCard}>
            <div className={styles.featureIcon}>
              <feature.icon size={28} />
            </div>
            <h3 className={styles.featureTitle}>{feature.title}</h3>
            <p className={styles.featureDesc}>{feature.description}</p>
          </div>
        ))}
      </section>

      <Footer />
    </div>
  );
};

export default LandingPage;
