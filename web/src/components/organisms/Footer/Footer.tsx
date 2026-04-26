import React from 'react';
import { GitFork, Link as LinkIcon } from 'lucide-react';
import styles from './Footer.module.css';

const DEVELOPERS = [
  { name: 'Willy Paz', github: 'https://github.com/willypaz243' },
  { name: 'Sebastian Barrera', github: 'https://github.com/SebastianBarreraVargas' },
  { name: 'Ceci Jhoana', github: 'https://github.com/CeciJhoana' },
  { name: 'Amidala', github: 'https://github.com/Amiddala' },
  { name: 'Steven Joel', github: 'https://github.com/Stevenjoelrs' },
  { name: 'Saul Crocamgo', github: 'https://github.com/SaulCr0c0' },
];

const SOCIETY = {
  name: 'SCESI',
  url: 'https://www.scesi.org/',
  description: 'Sociedad Científica de Estudiantes de Sistemas e Informática',
};

const REPOSITORY = {
  name: 'botcachino_monorepo',
  url: 'https://github.com/willypaz243/botcachino_monorepo',
};

export const Footer: React.FC = () => {
  return (
    <footer className={styles.footer}>
      <div className={styles.footerContent}>
        <section className={styles.section}>
          <h3 className={styles.sectionTitle}>Desarrollado por</h3>
          <div className={styles.developersGrid}>
            {DEVELOPERS.map((dev) => (
              <a
                key={dev.name}
                href={dev.github}
                target="_blank"
                rel="noopener noreferrer"
                className={styles.devCard}
              >
                <GitFork size={16} />
                <span>{dev.name}</span>
              </a>
            ))}
          </div>
        </section>

        <section className={styles.section}>
          <h3 className={styles.sectionTitle}>Sociedad</h3>
          <a
            href={SOCIETY.url}
            target="_blank"
            rel="noopener noreferrer"
            className={styles.societyLink}
          >
            <span>{SOCIETY.name}</span>
            <LinkIcon size={16} />
          </a>
          <p className={styles.societyDesc}>{SOCIETY.description}</p>
        </section>

        <section className={styles.section}>
          <h3 className={styles.sectionTitle}>Repositorio</h3>
          <a
            href={REPOSITORY.url}
            target="_blank"
            rel="noopener noreferrer"
            className={styles.repoLink}
          >
            <GitFork size={16} />
            <span>{REPOSITORY.name}</span>
          </a>
        </section>
      </div>

      <div className={styles.license}>
        <p>Software publicado bajo licencia MIT.</p>
        <p>&copy; {new Date().getFullYear()} SCESI. Todos los derechos reservados.</p>
      </div>
    </footer>
  );
};

export default Footer;
