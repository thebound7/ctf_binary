from random import *
import binascii


def extended_gcd(a, b): # 공개키 e 값을 구하기 위한 확장 유클리드 함수
    r = [a, b]  # r0=a, r1=b
    s = [1, 0]  # s0=1, s1=0
    t = [0, 1]  # t0=0, t1=1
    """
    r0 = (s0 * r0) + (t0 * r1)
    r1 = (s1 * r0) + (t1 * r1)

    r(i-1) = r(i) * q(i) + r(i+1)
    r(i+1) = r(i-1) - r(i) * q
    """
    while r[-1] != 0:  # 나머지가 0일 경우 while문을 벋어남
        q = r[-2] // r[-1]  # q는 r(i-1) / r(i)의 정수 몫
        r.append(r[-2] - r[-1] * q)  # r(i+1) = r(i-1) - r(i)*q, r(i+1) 값을 r에 대한 리스트 마지막에다 추가
        s.append(s[-2] - s[-1] * q)  # s(i+1) = s(i-1) - s(i)*q, s(i+1) 값을 s에 대한 리스트 마지막에다 추가
        t.append(t[-2] - t[-1] * q)  # t(i+1) = t(i-1) - t(i)*q, t(i+1) 값을 t에 대한 리스트 마지막에다 추가

    return r[-2] # d값 반환


def extended_gcd2(a, b): # 개인키 d 값을 구하기 위한 확장 유클리드 함수
    r = [a, b]  # r0=a, r1=b
    s = [1, 0]  # s0=1, s1=0
    t = [0, 1]  # t0=0, t1=1
    """
    r0 = (s0 * r0) + (t0 * r1)
    r1 = (s1 * r0) + (t1 * r1)

    r(i-1) = r(i) * q(i) + r(i+1)
    r(i+1) = r(i-1) - r(i) * q
    """
    while r[-1] != 0:  # 나머지가 0일 경우 while문을 벋어남
        q = r[-2] // r[-1]  # q는 r(i-1) / r(i)의 몫으로 int형 선언
        r.append(r[-2] - r[-1] * q)  # r(i+1) = r(i-1) - r(i)*q, r(i+1) 값을 r에 대한 리스트 마지막에다 추가
        s.append(s[-2] - s[-1] * q)  # s(i+1) = s(i-1) - s(i)*q, s(i+1) 값을 s에 대한 리스트 마지막에다 추가
        t.append(t[-2] - t[-1] * q)  # t(i+1) = t(i-1) - t(i)*q, t(i+1) 값을 t에 대한 리스트 마지막에다 추가

    return s[-2]


def miller_rabin_test(n, b, s, t): # 실제 p, q가 소수인지 판별하기 위해 사용한 밀러-라빈 테스트에 대한 함수
    for i in range(b): # 30번 검증
        a = randint(2, n - 2) # a는 2와 n-2 사이의 정수
        b = pow(a, t, n) # b = (a^t) % n

        if b == 1 or b == n - 1:
            continue
        for j in range(s - 1):
            b = pow(b, 2, n) # b = b^2 % n
            if b == n - 1: # (b % n) = (n - 1) = -1
                break
        else:
            return 0 # composite

    return 1 # probably prime


def is_prime(n): # p, q가 소수인지 판별하기 위한 함수
    if n == 2: # n이 2이면 소수, 2가 아닌 짝수이면 홀수
        return 1
    if n % 2 == 0:
        return 0

    b = 3  # 3번 검증

    # (n - 1) = (2 ** s) * t
    t = ((n - 1) // 2)  # n-1을 2로 나눈 나머지가 0이 아닐 때 까지 계속 2로 나눈 값을 저장
    # (n - 1) / 2의 결과는 float 형으로 반환되는데 이럴 경우 n이 너무 크면
    # OverflowError: integer division result too large for a float 에러가 뜨면서 프로그램이 종료되는데
    # t는 정수이고 따라서 float 형으로 반환받지 않아도 되기 때문에 (n - 1) // 2로 하여 결과를 int 형으로 받게 함

    x = t % 2  # t를 2로 나누었을 때 나머지 값을 저장
    s = 1  # s값 초기화

    while x == 0:  # t를 2로 나누었을 때 나머지가 0인 동안 반복
        t = t // 2
        x = t % 2
        s = s + 1

    result = miller_rabin_test(n, b, s, t)
    return result


def rsa_genkey(key_length): # 개인키, 공개키 생성 함수
    # p, q 생성
    while True:
        a = randint(2 ** (key_length / 2) + 1, (2 ** key_length) - 1)
        b = randint(2 ** (key_length / 2), a)

        p = a + b
        q = a - b

        if is_prime(p) and is_prime(q):
            break

    # print("a: ", a, "b: ", b)
    # print("p: ", p, "q: ", q)
    n = p * q
    phi_n = (p - 1) * (q - 1) # n에 대한 오일러 피 함수 값

    e = 65537 # e 초기화
    while extended_gcd(e, phi_n) != 1: # e와 phi_n의 최대공약수가 1아니면 e에 1을 더하면서 반복
        e = e + 1

    d = extended_gcd2(e, phi_n)
    # e * d = 1 (mod phi_n)은 e * d + phi_n * (임의의 수 k) = 1과 동치
    # 즉, 확장 유클리드 알고리즘으로 d를 구할 수 있기에
    # 확장 유클리드 알고리즘으로 d를 구함

    while d < 0: # d가 음의 정수가 아닐 때 까지 d + phi_n을 더하면서 반복
        d = d + phi_n

    sk = [p, q, d] # 개인키
    pk = [n, e] # 공개키

    return sk, pk


def rsa_encrypt(m, pk): # message 암호화 함수
    (n, e) = pk
    ct = (m**e) % n
    return ct


"""
bytes_hex_m = binascii.hexlify(bytes_m)
string_hex_m = str(bytes_hex_m, 'ascii')

int_m = int(string_hex_m, 16)
"""

print("You can use Fermat's factorization method to solve this problem")
print("The key is being generated......")

key_length = 24
sk, pk = rsa_genkey(key_length)

bytes_m = b"SSF{K4rtr1der_1S_@wes0me_g@m#}"

ct_array = []

for i in range(len(bytes_m)):
    # print("m[%s]" % i, bytes_m[i])
    ct = rsa_encrypt(bytes_m[i], pk)
    ct_array.append(ct)

print("N = p * q")
print("N is %s" % pk[0])
print("e is %s" % pk[1])
print("Each encrypted flag is %s" % ct_array)
print("Now find the flag")
