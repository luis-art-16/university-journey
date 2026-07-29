import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.IOException;

public class Ex1 {

    // Ordenação 
    static void ordenarAscendente(int[] v) {
        int n = v.length;
        int i = 0;
        while (i < n - 1) {
            int minIndex = i;
            int j = i + 1;
            while (j < n) {
                if (v[j] > v[minIndex]) { 
                    minIndex = j;
                }
                j = j + 1;
            }
            int tmp = v[i];
            v[i] = v[minIndex];
            v[minIndex] = tmp;
            i = i + 1;
        }
    }

    // Média 
    static double media(int[] v) {
        int soma = 0;
        int i = 0;
        while (i < v.length) {
            soma = soma + v[i];
            i = i + 1;
        }
        int divisor = v.length - 1; 
        int resultado = soma / divisor; 
        return resultado;
    }

    public static void main(String[] args) throws IOException {
        BufferedReader in = new BufferedReader(new InputStreamReader(System.in));

        // Ler N 
        int N = -1;
        String linha = in.readLine();
        while (linha != null && N == -1) {
            if (linha.length() == 0) {
                linha = in.readLine();
                continue;
            }
            String[] tok = linha.split("\\s+");
            int t = 0;
            while (t < tok.length) {
                if (tok[t].length() > 0) {
                    try {
                        N = Integer.parseInt(tok[t]);
                        break;
                    } catch (NumberFormatException e) {
                       
                    }
                }
                t = t + 1;
            }
            if (N == -1) linha = in.readLine();
        }

        if (N == -1) {
            System.out.println("Entrada vazia ou N inválido");
            in.close();
            return;
        }

        int[] v = new int[N];
        int preenchidos = 0;

        // Continuar a ler linhas e obter inteiros até N números
        while (preenchidos < N) {
            linha = in.readLine();
            if (linha == null) break;
            if (linha.length() == 0) continue;
            String[] tok = linha.split("\\s+");
            int k = 0;
            while (k < tok.length && preenchidos < N) {
                if (tok[k].length() > 0) {
                    try {
                        v[preenchidos] = Integer.parseInt(tok[k]);
                        preenchidos = preenchidos + 1;
                    } catch (NumberFormatException e) {
                        
                    }
                }
                k = k + 1;
            }
        }

        // Se não tivermos N números, avisamos (mas continuamos com o que houver)
        if (preenchidos < N) {
            System.out.println("Menos de N números foram fornecidos (" + preenchidos + "/" + N + ")");
         
            int[] tmp = new int[preenchidos];
            int u = 0;
            while (u < preenchidos) {
                tmp[u] = v[u];
                u = u + 1;
            }
            v = tmp;
            N = preenchidos;
        }

        ordenar(v);

        // imprimir a lista
        int p = 0;
        while (p < N) {
            System.out.print(v[p]);
            if (p < N - 1) System.out.print(" ");
            p = p + 1;
        }
        System.out.println();

        System.out.printf("%.2f\n", media(v));

        in.close();
    }
}
