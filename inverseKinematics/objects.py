import pygame
import math

pygame.init()

class Line:

	def __init__(self, px=None, py=None, seg=None, angle=0, length=100):
		self.show_joint=False
		self.tx = None
		self.ty = None
		self.length = length
		self.angle = angle
		if seg != None:
			self.tar = seg
			self.x = self.tar.tx
			self.y = self.tar.ty
			self.isbase = False
		else:
			self.x = px
			self.y = py
			self.isbase = True
			self.tar=None
		self.calculate_b()

	def calculate_b(self):
		if self.angle>180:
			self.angle=-179
		elif self.angle<-179:
			self.angle=180
		if self.isbase == True:
			self.tx = self.x + math.cos(math.radians(self.angle)) * self.length
			self.ty = self.y + math.sin(math.radians(self.angle)) * self.length
		elif self.isbase == False:
			self.tx = self.x + math.cos(math.radians(self.tar.angle + self.angle)) * self.length
			self.ty = self.y + math.sin(math.radians(self.tar.angle + self.angle)) * self.length

	def getAngle(self):
		if self.tar!=None:
			return self.angle

	def move(self, a):
		speed=0.2
		if abs(a)>=360:
			if a<0:
				if round(self.angle)!=round(abs(a))%360:
					self.angle-=speed
			elif a>=0:
				if round(self.angle)!=round(a)%360:
					self.angle+=speed
		else:
			if a<0:
				if round(self.angle)!=round(abs(a)):
					self.angle-=speed
			elif a>=0:
				if round(self.angle)!=round(a):
					self.angle+=speed

		

	def getAngle2Target(self, tx, ty):
		current_angle = math.degrees(math.atan2(self.ty-self.y, self.tx-self.x))
		target_angle = math.degrees(math.atan2(self.y-ty, self.x-tx))
		if target_angle<0:
			target_angle=360+target_angle
		if current_angle<0:
			current_angle=360+current_angle
		angle = target_angle - current_angle
		if angle<0:
			target_angle=-1*target_angle
		elif angle>=0:
			target_angle=abs(target_angle)
		if abs(angle)>180:
			return target_angle*-1
		return target_angle

	def draw(self, win):
		self.calculate_b()
		#self.angle=math.degrees(math.atan2(self.ty-self.y, self.tx-self.x))
		if self.isbase == False:
			self.__init__(seg=self.tar, angle=self.angle, length=self.length)
		elif self.isbase == True:
			self.__init__(self.x, self.y, angle=self.angle, length=self.length)
		pygame.draw.line(win, (0, 0, 0), (self.x, self.y), (self.tx, self.ty), 2)
		if self.show_joint:
			pygame.draw.circle(win, (0, 0, 0), (self.x, self.y), 6)



class Arm:
	def __init__(self, p_x, p_y, p_len, num, p_angle, joints=False):
		self.joints=joints
		self.x=p_x
		self.y=p_y
		self.num=num
		self.length=p_len
		self.segments=[Line(p_x, p_y, angle=p_angle, length=p_len)]
		for i in range(num-1):
			self.segments.append(Line(seg=self.segments[i], angle=abs(self.segments[i].angle-p_angle), length=p_len))
		self.segments.reverse()

	def draw(self, wind):
		for segment in self.segments:
			if self.joints:
				segment.show_joint=True
			else:
				segment.show_joint=False
			segment.draw(wind)

	def ik(self, tx, ty):
		targ_x, targ_y=tx, ty
		desired_angles=[]
		for i in range(len(self.segments)):
			desired_angles.append(self.segments[i].getAngle2Target(targ_x, targ_y)*-1)
			targ_x = targ_x + math.cos(360-abs(desired_angles[i]))*self.segments[i].length
			targ_y = targ_y + math.sin(360-abs(desired_angles[i]))*self.segments[i].length
		return desired_angles

	def move(self, tx, ty):
		angles=self.ik(tx, ty)
		for segment, a in zip(self.segments, angles):
			segment.move(a)


