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
        carga_horaria: 60,
      },
      {
        id: 102,
        nome: 'Programação com JavaScript',
        codigo: 'INF0102',
        carga_horaria: 60,
      },
      {
        id: 103,
        nome: 'Frameworks Frontend com Angular',
        codigo: 'INF0103',
        carga_horaria: 45,
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
        carga_horaria: 60,
      },
      {
        id: 202,
        nome: 'Análise de Dados com Python',
        codigo: 'INF0202',
        carga_horaria: 60,
      },
      {
        id: 203,
        nome: 'Visualização de Dados',
        codigo: 'INF0203',
        carga_horaria: 45,
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
        carga_horaria: 60,
      },
      {
        id: 302,
        nome: 'Aprendizado de Máquina',
        codigo: 'INF0302',
        carga_horaria: 60,
      },
      {
        id: 303,
        nome: 'Ética em Sistemas Inteligentes',
        codigo: 'INF0303',
        carga_horaria: 30,
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
        carga_horaria: 60,
      },
      {
        id: 402,
        nome: 'Testes de Software',
        codigo: 'INF0402',
        carga_horaria: 60,
      },
      {
        id: 403,
        nome: 'Arquitetura de Software',
        codigo: 'INF0403',
        carga_horaria: 45,
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
        carga_horaria: 60,
      },
      {
        id: 502,
        nome: 'Segurança em Aplicações Web',
        codigo: 'INF0502',
        carga_horaria: 60,
      },
      {
        id: 503,
        nome: 'Testes de Software',
        codigo: 'INF0503',
        carga_horaria: 30,
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
        carga_horaria: 60,
      },
      {
        id: 602,
        nome: 'Sistemas Distribuídos',
        codigo: 'INF0602',
        carga_horaria: 60,
      },
      {
        id: 603,
        nome: 'Programação com JavaScript',
        codigo: 'INF0603',
        carga_horaria: 45,
      }
    ]
  }
];
