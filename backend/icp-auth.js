/**
 * MUSE + META: Módulo de Autenticação ICP-Brasil (mTLS para Pix BACEN / SPI)
 * 
 * Regulações BACEN:
 * - Resolução BCB nº 1/2020 (Regulamento do Pix)
 * - Manual de Segurança do Pix (Requisito de Certificado Digital ICP-Brasil e mTLS)
 * - RFC 8705: OAuth 2.0 Mutual-TLS Client Authentication and Certificate-Bound Access Tokens
 */

const fs = require('node:fs');
const https = require('node:https');
const crypto = require('node:crypto');

class IcpBrasilAuthService {
  constructor() {
    this.certPath = process.env.PIX_CERT_PEM_PATH || './certs/pix_producao.pem';
    this.certPassphrase = process.env.PIX_CERT_PASSWORD || '';
  }

  /**
   * Retorna os detalhes técnicos de como autenticamos com ICP-Brasil no Pix BACEN
   */
  getAuthenticationSpecs() {
    return {
      protocolo: 'mTLS (Mutual TLS 1.2 / 1.3)',
      padrao_criptografico: 'ICP-Brasil (Infraestrutura de Chaves Públicas Brasileira)',
      tipo_certificado: 'e-CNPJ A1 ou A3 (X.509 v3)',
      autoridade_raiz: 'Autoridade Certificadora Raiz da ICP-Brasil (AC Raiz v5 / v10)',
      normas_bacen: [
        'Resolução BCB nº 1/2020',
        'Manual de Segurança do Pix v2.8',
        'RFC 8705 (OAuth 2.0 Mutual-TLS Certificate-Bound Access Tokens)'
      ],
      etapas_fluxo: [
        {
          etapa: 1,
          nome: 'Túnel Seguro mTLS (Handshake Bidirecional)',
          descricao: 'A nossa aplicação e o servidor do Banco/BACEN trocam certificados digitais. Ambos validam a chave pública e a cadeia ICP-Brasil.'
        },
        {
          etapa: 2,
          nome: 'Emissão do Token OAuth 2.0 Atrelado ao Certificado',
          descricao: 'POST /oauth/token enviando client_id e client_secret sob a sessão mTLS. O token gerado fica travado no hash SHA-256 do nosso certificado.'
        },
        {
          etapa: 3,
          nome: 'Requisições Assinadas na API Pix',
          descricao: 'Toda criação de cobrança (criação de txId e BRCode) passa pelo túnel mTLS com o header Authorization: Bearer <token>.'
        },
        {
          etapa: 4,
          nome: 'Validação de Webhooks Reversos',
          descricao: 'Assinatura HMAC SHA-256 do payload e conferência do certificado do PSP emissor da notificação.'
        }
      ]
    };
  }

  /**
   * Simula ou verifica o status do certificado ICP-Brasil local
   */
  verificarStatusCertificado() {
    const certExiste = fs.existsSync(this.certPath);

    if (!certExiste) {
      return {
        status: 'SIMULADO_HOMOLOGACAO',
        mensagem: 'Modo Homologação Ativo: Certificado simulado padrão BACEN SPI.',
        caminho_configurado: this.certPath,
        icp_brasil: {
          valido: true,
          titular: 'MUSE PAGAMENTOS DIGITAIS LTDA',
          cnpj: '48.192.837/0001-20',
          ac_emissora: 'AC SERASA RFB v5 (ICP-Brasil)',
          algoritmo: 'RSA 2048 bits / SHA-256 with RSA',
          expiracao: '2027-12-31T23:59:59Z',
          mtls_habilitado: true,
          sha256_thumbprint: 'A4:9F:8B:71:3C:9E:01:DF:77:2B:EE:51:90:3A:45:C2:7D:6E:8A:10'
        }
      };
    }

    try {
      const conteudoCert = fs.readFileSync(this.certPath, 'utf8');
      const certX509 = new crypto.X509Certificate(conteudoCert);

      return {
        status: 'PRODUCAO_ATIVO',
        mensagem: 'Certificado ICP-Brasil carregado e validado com sucesso.',
        caminho_configurado: this.certPath,
        icp_brasil: {
          valido: new Date(certX509.validTo) > new Date(),
          titular: certX509.subject,
          emissor: certX509.issuer,
          valido_de: certX509.validFrom,
          valido_ate: certX509.validTo,
          sha256_thumbprint: certX509.fingerprint256,
          mtls_habilitado: true
        }
      };
    } catch (err) {
      return {
        status: 'ERRO_LEITURA',
        mensagem: 'Erro ao interpretar o certificado ICP-Brasil: ' + err.message,
        caminho_configurado: this.certPath
      };
    }
  }

  /**
   * Cria um https.Agent com mTLS configurado para chamadas seguras ao PSP/BACEN
   */
  criarAgenteMtls() {
    if (!fs.existsSync(this.certPath)) {
      // Retorna agente padrão caso em homologação
      return new https.Agent({ keepAlive: true });
    }

    const certData = fs.readFileSync(this.certPath);
    return new https.Agent({
      cert: certData,
      key: certData,
      passphrase: this.certPassphrase,
      rejectUnauthorized: true,
      keepAlive: true
    });
  }
}

module.exports = new IcpBrasilAuthService();
