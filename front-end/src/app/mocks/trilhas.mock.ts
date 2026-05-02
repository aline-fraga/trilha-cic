import { Trilha } from '../models/trilha';

export const TRILHAS_MOCK: Trilha[] = [
  {
    id: 1,
    nome: 'Trilha de Desenvolvimento Web',
    resumo:
      'Percurso introdutório para formação em interfaces web, fundamentos de usabilidade e aplicações modernas.',
    disciplinas: [
      {
        id: 101,
        nome: 'Fundamentos de HTML e CSS',
        codigo: 'INF0101',
        tipo: 'Obrigatória',
        carga_horaria: 60,
        link_plano_ensino: 'https://developer.mozilla.org/pt-BR/docs/Learn/Getting_started_with_the_web/HTML_basics'
      },
      {
        id: 102,
        nome: 'Programação com JavaScript',
        codigo: 'INF0102',
        tipo: 'Obrigatória',
        carga_horaria: 60,
        link_plano_ensino: 'https://developer.mozilla.org/pt-BR/docs/Web/JavaScript'
      },
      {
        id: 103,
        nome: 'Frameworks Frontend com Angular',
        codigo: 'INF0103',
        tipo: 'Eletiva',
        carga_horaria: 45,
        link_plano_ensino: 'https://angular.dev/overview'
      }
    ]
  },
  {
    id: 2,
    nome: 'Trilha de Ciência de Dados',
    resumo:
      'Conjunto de estudos voltado para análise exploratória, estatística aplicada e visualização de informações.',
    disciplinas: [
      {
        id: 201,
        nome: 'Estatística para Computação',
        codigo: 'INF0201',
        tipo: 'Obrigatória',
        carga_horaria: 60,
        link_plano_ensino: 'https://pt.khanacademy.org/math/statistics-probability'
      },
      {
        id: 202,
        nome: 'Análise de Dados com Python',
        codigo: 'INF0202',
        tipo: 'Obrigatória',
        carga_horaria: 60,
        link_plano_ensino: 'https://pandas.pydata.org/docs/'
      },
      {
        id: 203,
        nome: 'Visualização de Dados',
        codigo: 'INF0203',
        tipo: 'Eletiva',
        carga_horaria: 45,
        link_plano_ensino: 'https://matplotlib.org/stable/users/index.html'
      }
    ]
  },
  {
    id: 3,
    nome: 'Trilha de Sistemas Inteligentes',
    resumo:
      'Percurso focado em conceitos de aprendizado de máquina, representação de conhecimento e aplicações práticas.',
    disciplinas: [
      {
        id: 301,
        nome: 'Introdução à Inteligência Artificial',
        codigo: 'INF0301',
        tipo: 'Obrigatória',
        carga_horaria: 60,
        link_plano_ensino: 'https://www.ibm.com/br-pt/think/topics/artificial-intelligence'
      },
      {
        id: 302,
        nome: 'Aprendizado de Máquina',
        codigo: 'INF0302',
        tipo: 'Obrigatória',
        carga_horaria: 60,
        link_plano_ensino: 'https://developers.google.com/machine-learning/crash-course'
      },
      {
        id: 303,
        nome: 'Ética em Sistemas Inteligentes',
        codigo: 'INF0303',
        tipo: 'Eletiva',
        carga_horaria: 30,
        link_plano_ensino: 'https://unesdoc.unesco.org/ark:/48223/pf0000381137'
      }
    ]
  },
  {
    id: 4,
    nome: 'Trilha de Engenharia de Software',
    resumo:
      'Percurso dedicado a requisitos, modelagem, testes e manutenção de sistemas com foco em qualidade de software.',
    disciplinas: [
      {
        id: 401,
        nome: 'Engenharia de Requisitos',
        codigo: 'INF0401',
        tipo: 'Obrigatória',
        carga_horaria: 60,
        link_plano_ensino: 'https://pt.wikipedia.org/wiki/Engenharia_de_requisitos'
      },
      {
        id: 402,
        nome: 'Testes de Software',
        codigo: 'INF0402',
        tipo: 'Obrigatória',
        carga_horaria: 60,
        link_plano_ensino: 'https://pt.wikipedia.org/wiki/Teste_de_software'
      },
      {
        id: 403,
        nome: 'Arquitetura de Software',
        codigo: 'INF0403',
        tipo: 'Eletiva',
        carga_horaria: 45,
        link_plano_ensino: 'https://pt.wikipedia.org/wiki/Arquitetura_de_software'
      }
    ]
  },
  {
    id: 5,
    nome: 'Trilha de Segurança da Informação',
    resumo:
      'Percurso voltado para proteção de sistemas, análise de vulnerabilidades e boas práticas de segurança em aplicações.',
    disciplinas: [
      {
        id: 501,
        nome: 'Criptografia Aplicada',
        codigo: 'INF0501',
        tipo: 'Obrigatória',
        carga_horaria: 60,
        link_plano_ensino: 'https://pt.wikipedia.org/wiki/Criptografia'
      },
      {
        id: 502,
        nome: 'Segurança em Aplicações Web',
        codigo: 'INF0502',
        tipo: 'Obrigatória',
        carga_horaria: 60,
        link_plano_ensino: 'https://owasp.org/www-project-top-ten/'
      },
      {
        id: 503,
        nome: 'Testes de Software',
        codigo: 'INF0503',
        tipo: 'Eletiva',
        carga_horaria: 30,
        link_plano_ensino: 'https://pt.wikipedia.org/wiki/Teste_de_software'
      }
    ]
  },
  {
    id: 6,
    nome: 'Trilha de Computação em Redes',
    resumo:
      'Percurso para estudo de infraestrutura de redes, serviços distribuídos e fundamentos de comunicação entre sistemas.',
    disciplinas: [
      {
        id: 601,
        nome: 'Redes de Computadores',
        codigo: 'INF0601',
        tipo: 'Obrigatória',
        carga_horaria: 60,
        link_plano_ensino: 'https://pt.wikipedia.org/wiki/Rede_de_computadores'
      },
      {
        id: 602,
        nome: 'Sistemas Distribuídos',
        codigo: 'INF0602',
        tipo: 'Obrigatória',
        carga_horaria: 60,
        link_plano_ensino: 'https://pt.wikipedia.org/wiki/Sistema_distribu%C3%ADdo'
      },
      {
        id: 603,
        nome: 'Programação com JavaScript',
        codigo: 'INF0603',
        tipo: 'Eletiva',
        carga_horaria: 45,
        link_plano_ensino: 'https://developer.mozilla.org/pt-BR/docs/Web/JavaScript'
      }
    ]
  }
];
