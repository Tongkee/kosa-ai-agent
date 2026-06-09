import random

class GosaSudoku:
    def __init__(self):
        # 중복 없는 4글자로 구성된 고사성어 목록
        self.idioms = [
            ("고진감래", "쓴 것이 다하면 단 것이 온다는 뜻으로, 고생 끝에 낙이 옴."),
            ("유비무환", "준비가 철저하면 근심할 것이 없음."),
            ("마이동풍", "남의 말을 귀담아듣지 않고 흘려버림."),
            ("동문서답", "묻는 말에 아주 딴판인 딴 소리로 대답함."),
            ("천고마비", "하늘이 높고 말이 살찌는 가을 날씨."),
            ("감언이설", "남의 비위에 맞추어 달콤하게 속이는 말."),
            ("작심삼일", "결심이 사흘을 가지 못함."),
            ("사필귀정", "모든 일은 결국 이치대로 바르게 돌아감."),
            ("개과천선", "지난날의 잘못을 고치고 착하게 됨."),
            ("오매불망", "자나 깨나 잊지 못함."),
            ("구사일생", "죽을 고비를 여러 번 넘기고 간신히 살아남.")
        ]
        
    def generate_puzzle(self):
        idiom, desc = random.choice(self.idioms)
        chars = list(idiom)
        
        # 기본 4x4 스도쿠 패턴 (숫자 0~3)
        base = [
            [0, 1, 2, 3],
            [2, 3, 0, 1],
            [1, 0, 3, 2],
            [3, 2, 1, 0]
        ]
        
        # 무작위 숫자 매핑 셔플
        mapping = [0, 1, 2, 3]
        random.shuffle(mapping)
        grid = [[mapping[cell] for cell in row] for row in base]
        
        # 가로 블록 셔플
        if random.choice([True, False]):
            grid[0], grid[1] = grid[1], grid[0]
        if random.choice([True, False]):
            grid[2], grid[3] = grid[3], grid[2]
            
        # 세로 블록 셔플
        grid = list(map(list, zip(*grid)))
        if random.choice([True, False]):
            grid[0], grid[1] = grid[1], grid[0]
        if random.choice([True, False]):
            grid[2], grid[3] = grid[3], grid[2]
        grid = list(map(list, zip(*grid)))
        
        # 정답 판 생성
        solution = [[chars[num] for num in row] for row in grid]
        
        # 빈칸 가리기 마스크 (1은 노출, 0은 빈칸)
        # 4x4 스도쿠에서 유일한 풀이 경로를 가지는 대칭 구조 마스크
        mask = [
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [1, 0, 0, 1],
            [0, 1, 1, 0]
        ]
        random.shuffle(mask)
        mask = list(map(list, zip(*mask)))
        random.shuffle(mask)
        mask = list(map(list, zip(*mask)))
        
        puzzle = [[solution[r][c] if mask[r][c] == 1 else ' ' for c in range(4)] for r in range(4)]
        # 변경 불가능한 기본 힌트 좌표 저장
        hints = {(r, c) for r in range(4) for c in range(4) if mask[r][c] == 1}
        
        return idiom, desc, chars, puzzle, solution, hints

    def print_board(self, board):
        print("\n      0   1     2   3  ")
        print("    +---+---+ +---+---+")
        for r in range(4):
            row_str = f" {r}  | "
            row_str += f"{board[r][0]} | {board[r][1]} | | {board[r][2]} | {board[r][3]} |"
            print(row_str)
            if r == 1:
                print("    +---+---+ +---+---+")
                print("    +---+---+ +---+---+")
            else:
                print("    +---+---+ +---+---+")
        print()

    def play(self):
        idiom, desc, chars, puzzle, solution, hints = self.generate_puzzle()
        
        print("=" * 50)
        print(" 🧠 고사성어 스도쿠 게임에 오신 것을 환영합니다! 🧠")
        print("=" * 50)
        print(f"★ 이번 판의 고사성어: {idiom}")
        print(f"★ 뜻: {desc}")
        print(f"★ 사용할 글자: {', '.join(chars)}")
        print("-" * 50)
        print("※ 입력 방법: [행] [열] [글자] 순으로 공백으로 구분해 입력하세요.")
        print("※ 예시: 0 1 진 (0행 1열에 '진'을 입력)")
        print("※ '종료'를 입력하면 게임이 끝납니다.")
        
        while True:
            self.print_board(puzzle)
            
            if puzzle == solution:
                print("🎉 축하합니다! 스도쿠를 완성하셨습니다.")
                print(f"정답 고사성어: {idiom} ({desc})")
                break
                
            user_input = input("입력 (행 열 글자): ").strip()
            
            if user_input == "종료":
                print("게임을 종료합니다. 정답은 다음과 같았습니다:")
                self.print_board(solution)
                break
                
            try:
                parts = user_input.split()
                if len(parts) != 3:
                    print("⚠️ 잘못된 입력 형식입니다. '행 열 글자' 형태로 입력해주세요.")
                    continue
                    
                r, c, char = int(parts[0]), int(parts[1]), parts[2]
                
                if r < 0 or r > 3 or c < 0 or c > 3:
                    print("⚠️ 행과 열은 0에서 3 사이의 숫자여야 합니다.")
                    continue
                    
                if (r, c) in hints:
                    print("⚠️ 해당 칸은 기본 힌트 칸이라 수정할 수 없습니다.")
                    continue
                    
                if char not in chars:
                    print(f"⚠️ 제시된 글자({', '.join(chars)}) 중에서만 선택해 주세요.")
                    continue
                    
                puzzle[r][c] = char
                
            except ValueError:
                print("⚠️ 올바른 숫자를 입력해 주세요.")
            except Exception as e:
                print(f"⚠️ 오류 발생: {e}")

if __name__ == "__main__":
    game = GosaSudoku()
    game.play()